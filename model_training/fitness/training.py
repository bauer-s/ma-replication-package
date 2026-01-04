import os
import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score


"""Optimized training script to reduce wall time on SLURM.
Changes vs original:
- Replaces exhaustive GridSearchCV with RandomizedSearchCV (n_iter=20)
- Early stopping enabled (early_stopping=True, validation_fraction=0.1)
- Smaller, higher-signal hyperparameter space
- Parallel evaluation (n_jobs=4) to match --cpus-per-task
- Optional subsampling via SAMPLE_FRAC env var for quick prototyping
- Saves best model + scaler (mlp_best.joblib) and an append-only summary file
"""

df_path = "../df.pickle"


def get_x_y_from_df(df_name: str):
    df = pd.read_pickle(df_name)
    df.dropna(how='any', inplace=True)
    df.drop(['hashCode'], axis=1, inplace=True, errors='ignore')
    df.reset_index(inplace=True, drop=True)
    X = df.filter(regex=("project*"))
    y = df["fitness"].values.ravel()
    return X, y


print('Get Dataframe')
X, y = get_x_y_from_df(df_path)

# Train/test split with fixed seed for reproducibility
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Optional subsampling (only training set) for faster experimentation
sample_frac = float(os.environ.get("SAMPLE_FRAC", "1.0"))
if sample_frac < 1.0:
    rs = np.random.RandomState(42)
    subset_idx = rs.choice(len(X_train), size=max(1, int(len(X_train) * sample_frac)), replace=False)
    X_train = X_train.iloc[subset_idx]
    y_train = y_train[subset_idx]
    print(f"Subsampled training set to {sample_frac*100:.1f}% -> {len(X_train)} samples")

# Scale features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

print("Shapes: X_train", X_train.shape, "X_test", X_test.shape)

# Focused hyperparameter distributions
param_grid = {
    'hidden_layer_sizes': [(100,), (128,), (64, 64), (128, 64), (64, 128)],
    'activation': ['relu', 'tanh'],
    'alpha': [1e-5, 1e-4, 1e-3, 1e-2],
    'learning_rate': ['constant', 'adaptive'],
    'solver': ['adam', 'sgd'],
}

base_model = MLPRegressor(
    max_iter=300,
    early_stopping=True,
    n_iter_no_change=10,
    validation_fraction=0.1,
    random_state=42,
)

search = GridSearchCV(
    estimator=base_model,
    param_grid=param_grid,
    n_jobs=4,
    verbose=2,
    cv=3,
)

print('Fit model to data (GridSearchCV)')
search.fit(X_train, y_train)

# Save all grid search results for further analysis
results_df = pd.DataFrame(search.cv_results_)
results_df.to_csv('grid_search_results.csv', index=False)
print('Saved all grid search results to grid_search_results.csv')

print('Best parameters found:\n', search.best_params_)
print(f"Best CV score: {search.best_score_:.4f}")

# Save artifacts for reuse
artifacts = {
    'best_params': search.best_params_,
    'best_score': search.best_score_,
    'scaler': scaler,
    'model': search.best_estimator_,
}
joblib.dump(artifacts, 'mlp_best.joblib')
print('Saved best model to mlp_best.joblib')

# Evaluate on held-out test set
y_true, y_pred = y_test, search.predict(X_test)
test_r2 = r2_score(y_true, y_pred)
print('Results on the test set (R2):', test_r2)

with open('training_summary.txt', 'a', encoding='utf-8') as fh:
    fh.write(
        f"Run summary: test_r2={test_r2:.4f} best_cv={search.best_score_:.4f} params={search.best_params_}\n"
    )
print('Appended run summary to training_summary.txt')

