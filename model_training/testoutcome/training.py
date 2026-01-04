import os
import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score


def get_x_y_from_df(df_name: str):
    df = pd.read_pickle(df_name)
    df.dropna(how='any', inplace=True)
    df.drop(['numPass', 'numFail', 'hashCode', 'fitness'], axis=1, inplace=True, errors='ignore')
    df.reset_index(inplace=True, drop=True)
    X = df.filter(regex=("project*"))
    y = df.filter(regex=("test*"))
    return X, y

print('Get Dataframe')
X, y = get_x_y_from_df("../df.pickle")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Optional subsampling (only training set) for faster experimentation
sample_frac = float(os.environ.get("SAMPLE_FRAC", "1.0"))
if sample_frac < 1.0:
    rs = np.random.RandomState(42)
    subset_idx = rs.choice(len(X_train), size=max(1, int(len(X_train) * sample_frac)), replace=False)
    X_train = X_train.iloc[subset_idx]
    y_train = y_train.iloc[subset_idx]
    print(f"Subsampled training set to {sample_frac*100:.1f}% -> {len(X_train)} samples")

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

y_train = y_train.astype(dtype=int)
y_test = y_test.astype(dtype=int)

print("Shapes: X_train", X_train.shape, "X_test", X_test.shape)
print("Shapes: y_train", y_train.shape, "y_test", y_test.shape)

param_grid = {
    'hidden_layer_sizes': [(100,), (128,), (64, 64), (128, 64), (64, 128)],
    'activation': ['relu', 'tanh'],
    'alpha': [0.0001, 0.001],
    'learning_rate': ['constant', 'adaptive'],
}

base_model = MLPClassifier(
    max_iter=300,
    early_stopping=True,
    n_iter_no_change=10,
    validation_fraction=0.1,
    random_state=42,
)

clf = GridSearchCV(
    estimator=base_model,
    param_grid=param_grid,
    cv=3,
    refit=True,
    verbose=2,
    n_jobs=4,
)

print('Fit model to data (GridSearchCV)')
clf.fit(X_train, y_train)

# Save all grid search results for further analysis
results_df = pd.DataFrame(clf.cv_results_)
results_df.to_csv('grid_search_results.csv', index=False)
print('Saved all grid search results to grid_search_results.csv')

# Best parameter set
print('Best parameters found:\n', clf.best_params_)
print(f"Best CV score: {clf.best_score_:.4f}")

# Save artifacts for reuse
artifacts = {
    'best_params': clf.best_params_,
    'best_score': clf.best_score_,
    'scaler': scaler,
    'model': clf.best_estimator_,
}
joblib.dump(artifacts, 'mlp_classifier_best.joblib')
print('Saved best model to mlp_classifier_best.joblib')

# All results
means = clf.cv_results_['mean_test_score']
stds = clf.cv_results_['std_test_score']
for mean, std, params in zip(means, stds, clf.cv_results_['params']):
    print("%0.3f (+/-%0.03f) for %r" % (mean, std * 2, params))

print()

y_true, y_pred = y_test, clf.predict(X_test)
test_acc = accuracy_score(y_true, y_pred)
print('Results on the test set (accuracy):', test_acc)

with open('classification_training_summary.txt', 'a', encoding='utf-8') as fh:
    fh.write(
        f"Run summary: test_acc={test_acc:.4f} best_cv={clf.best_score_:.4f} params={clf.best_params_}\n"
    )
print('Appended run summary to classification_training_summary.txt')

print()
print("y_true")
print(y_true)
print("y_pred")
print(y_pred)


