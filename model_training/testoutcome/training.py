import os
import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, hamming_loss, f1_score


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

y_train = y_train.astype(dtype=int).values
y_test = y_test.astype(dtype=int).values

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
    scoring='f1_micro',
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
print(f"Best CV score (F1 micro): {clf.best_score_:.4f}")

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

# Calculate multiple metrics for evaluation
exact_match_acc = accuracy_score(y_true, y_pred)
hamming = hamming_loss(y_true, y_pred)
per_label_acc = 1 - hamming
f1_micro = f1_score(y_true, y_pred, average='micro', zero_division=0)
f1_macro = f1_score(y_true, y_pred, average='macro', zero_division=0)

print('='*80)
print('RESULTS ON TEST SET:')
print('='*80)
print(f'Exact Match Accuracy:  {exact_match_acc:.4f} ({exact_match_acc*100:.2f}%)')
print(f'Hamming Loss:          {hamming:.4f}')
print(f'Per-Label Accuracy:    {per_label_acc:.4f} ({per_label_acc*100:.2f}%)')
print(f'F1 Score (micro):      {f1_micro:.4f}')
print(f'F1 Score (macro):      {f1_macro:.4f}')
print('='*80)

# Calculate per-test accuracies
per_test_accuracies = []
for i in range(y_true.shape[1]):
    test_acc = accuracy_score(y_true[:, i], y_pred[:, i])
    per_test_accuracies.append(test_acc)

print(f'\nPer-Test Accuracy Statistics:')
print(f'  Mean: {np.mean(per_test_accuracies):.4f} ({np.mean(per_test_accuracies)*100:.2f}%)')
print(f'  Min:  {np.min(per_test_accuracies):.4f} ({np.min(per_test_accuracies)*100:.2f}%)')
print(f'  Max:  {np.max(per_test_accuracies):.4f} ({np.max(per_test_accuracies)*100:.2f}%)')
print(f'  Std:  {np.std(per_test_accuracies):.4f}')

with open('classification_training_summary.txt', 'a', encoding='utf-8') as fh:
    fh.write(f"Run summary: exact_match={exact_match_acc:.4f} per_label_acc={per_label_acc:.4f} "
             f"hamming_loss={hamming:.4f} f1_micro={f1_micro:.4f} f1_macro={f1_macro:.4f} "
             f"best_cv_f1_micro={clf.best_score_:.4f} params={clf.best_params_}\n")
print('Appended run summary to classification_training_summary.txt')

print()
print("y_true")
print(y_true)
print("y_pred")
print(y_pred)


