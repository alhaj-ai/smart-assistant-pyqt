from pathlib import Path
import yaml, joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

DATA = Path(__file__).with_name("training_data.yaml")
OUT_DIR = Path(__file__).with_name("models")
OUT_DIR.mkdir(exist_ok=True)

def load_samples():
    y, X = [], []
    data = yaml.safe_load(DATA.read_text(encoding="utf-8"))
    for item in data["intents"]:
        intent = item["intent"]
        for txt in item["texts"]:
            y.append(intent)
            X.append(txt)
    return X, y

def train():
    X, y = load_samples()
    vec = TfidfVectorizer(ngram_range=(1,2), min_df=1, max_features=4000)
    clf = LogisticRegression(max_iter=300)
    Xv = vec.fit_transform(X)
    clf.fit(Xv, y)
    joblib.dump(vec, OUT_DIR/"tfidf.joblib")
    joblib.dump(clf, OUT_DIR/"intent_clf.joblib")
    print("Saved models to:", OUT_DIR)

if __name__ == "__main__":
    train()
