import pandas as pd
import seaborn as sns
sns.set()

df = pd.read_csv('creditcard.csv')
print(df.shape)
df.head()

df.info()

df.describe()

class_names = {0:'Not Fraud', 1:'Fraud'}
print(df.Class.value_counts().rename(index = class_names))

from sklearn.model_selection import train_test_split

feature_names = df.iloc[:, 1:30].columns
target = df.iloc[:1, 30: ].columns
print(feature_names)
print(target)

data_features = df[feature_names]
data_target = df[target]

X_train, X_test, y_train, y_test = train_test_split(data_features, data_target, train_size=0.70, test_size=0.30, random_state=1)
print("Length of X_train is: {X_train}".format(X_train = len(X_train)))
print("Length of X_test is: {X_test}".format(X_test = len(X_test)))
print("Length of y_train is: {y_train}".format(y_train = len(y_train)))
print("Length of y_test is: {y_test}".format(y_test = len(y_test)))

from sklearn.linear_model import LogisticRegression

model = LogisticRegression()
model.fit(X_train, y_train.values.ravel())

pred = model.predict(X_test)

# Loop through the DataFrame and make predictions for each row
for index, row in df.iterrows():
    # Keep the row in DataFrame format to maintain feature names
    row_data = pd.DataFrame([row[feature_names]])
    prediction = model.predict(row_data)
    # Extract actual target value for the current row
    actual_target = row[data_target.columns[0]]
    if actual_target == 1.0:
        # Print the entire row, actual target, and the prediction
        print(f"Row: {row.to_dict()}, Actual Target: {class_names[actual_target]}, Prediction: {class_names[prediction[0]]}")
