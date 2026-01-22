import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

os.makedirs("model", exist_ok=True)

df = pd.read_csv("data/resume_dataset.csv")
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(df['resume_text'])
y = df['label']

model = LogisticRegression(max_iter=1000)
model.fit(X, y)

joblib.dump((model, vectorizer), "model/resume_classifier.pkl")
print("Model trained successfully")