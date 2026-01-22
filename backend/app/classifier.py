import joblib
from app.preprocess import clean_text

model, vectorizer = joblib.load("model/resume_classifier.pkl")

ROLE_KEYWORDS = {
    "AI/ML Engineer": ["machine learning", "deep learning", "tensorflow", "pytorch", "nlp"],
    "Data Scientist": ["data analysis", "statistics", "pandas", "numpy", "sql"],
    "Web Developer": ["html", "css", "javascript", "react", "frontend"],
    "Software Engineer": ["java", "spring", "backend", "api", "microservices"],
    "DevOps/Cloud Engineer": ["aws", "docker", "kubernetes", "ci/cd"],
    "FullStack Developer": ["react", "node", "mongodb", "express"]
}

def classify_resume(text):
    text_clean = clean_text(text)

    # 1️⃣ ML prediction
    X = vectorizer.transform([text_clean])
    probs = model.predict_proba(X)[0]
    ml_role = model.classes_[probs.argmax()]
    ml_conf = probs.max()

    # 2️⃣ Keyword boosting
    keyword_scores = {}
    for role, keywords in ROLE_KEYWORDS.items():
        keyword_scores[role] = sum(
            1 for kw in keywords if kw in text_clean
        )

    best_rule_role = max(keyword_scores, key=keyword_scores.get)
    rule_score = keyword_scores[best_rule_role]

    # 3️⃣ Hybrid decision
    if rule_score >= 3:
        final_role = best_rule_role
        confidence = min(0.95, 0.6 + rule_score * 0.1)
    else:
        final_role = ml_role
        confidence = ml_conf

    return final_role, round(confidence, 2)
