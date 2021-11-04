from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import recall_score
from sklearn.model_selection import train_test_split, KFold
import pandas as pd


df = pd.read_parquet('./rus_df.parquet')
drop_dup_df = df.drop_duplicates()
drop_dup_df.groupby('is_plagiarism').describe()
X_train, X_val, y_train, y_val = train_test_split(
    drop_dup_df.loc[:, ['cosine_similarity']], drop_dup_df.loc[:, 'is_plagiarism']
)
print(y_train.value_counts())
y_val.value_counts()

test_models = [
             {'estimator': SVC, 'params': {'C': 0.01, 'kernel': 'linear'}},
             {'estimator': SVC, 'params': {'C': 0.01, 'kernel': 'rbf'}},
             {'estimator': SVC, 'params': {'C': 1, 'kernel': 'linear'}},
             {'estimator': SVC, 'params': {'C': 1, 'kernel': 'rbf'}},
             {'estimator': SVC, 'params': {'C': 10, 'kernel': 'linear'}},
             {'estimator': SVC, 'params': {'C': 10, 'kernel': 'rbf'}},
             {'estimator': LogisticRegression, 'params': {}}
]


best_model = None
best_score = 0
K = 5
kf = KFold(K, random_state=14, shuffle=True)
for test_model in test_models:
    total_recall = 0
    model = test_model['estimator'](**test_model['params'])
    for train_index, test_index in kf.split(X_train):
        X, y = X_train.iloc[train_index, :], y_train.iloc[train_index]
        X_test, y_test = X_train.iloc[test_index, :], y_train.iloc[test_index]

        model.fit(X, y)
        y_pred = model.predict(X_test)

        score = recall_score(y_test, y_pred)
        total_recall += score
        mean_recall = round(total_recall / K, 5)
        if mean_recall > best_score:
            best_score = mean_recall
            best_model = test_model
    print('Model: {} -- Params: {} -- Score: {}'.format(
        test_model['estimator'], test_model['params'], mean_recall)
    )

print('Best score: {}'.format(best_score))
print('Best model: {}'.format(best_model))


clf = best_model['estimator'](**best_model['params'])
clf.fit(X_train, y_train)
y_pred = clf.predict(X_val)
recall_score(y_val, y_pred)