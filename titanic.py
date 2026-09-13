import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder

train = pd.read_csv("train.csv")
test = pd.read_csv("test.csv")

test_ids = test["PassengerId"]

def preprocess(df):
    df = df.copy()
    df.drop(columns=["Cabin", "Ticket", "Name", "PassengerId"], inplace=True)
    df["Age"] = df["Age"].fillna(df["Age"].median())
    df["Fare"] = df["Fare"].fillna(df["Fare"].median())
    df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode()[0])
    le_sex = LabelEncoder()
    df["Sex"] = le_sex.fit_transform(df["Sex"])
    le_emb = LabelEncoder()
    df["Embarked"] = le_emb.fit_transform(df["Embarked"])
    return df

train_processed = preprocess(train)
test_processed = preprocess(test)

X = train_processed.drop(columns=["Survived"])
y = train_processed["Survived"]

model = DecisionTreeClassifier(max_depth=5, random_state=42)
model.fit(X, y)

predictions = model.predict(test_processed)

submission = pd.DataFrame({
    "PassengerId": test_ids,
    "Survived": predictions
})
submission.to_csv("submission.csv", index=False)
print("submission.csv gerado com sucesso!")
