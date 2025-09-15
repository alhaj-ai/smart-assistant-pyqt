from pathlib import Path
import joblib

MODELS_DIR = Path(__file__).with_name("models")
VEC = joblib.load(MODELS_DIR/"tfidf.joblib")
CLF = joblib.load(MODELS_DIR/"intent_clf.joblib")

def ml_predict_intent(text: str) -> tuple[str, float]:
    Xv = VEC.transform([text])
    proba = CLF.predict_proba(Xv)[0]
    idx = proba.argmax()
    return CLF.classes_[idx], float(proba[idx])
