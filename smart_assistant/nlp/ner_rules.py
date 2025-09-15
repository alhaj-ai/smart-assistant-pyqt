import json
from pathlib import Path

# كلمات ربط/حشو
STOP = {"عن","على","في","من","الى","إلى","بخصوص","لي","له","لها","لك","لهم","لنا","لو","من فضلك","لو سمحت"}

# استهداف تطبيق/موقع بالاسم/المرادفات عبر apps.json
def _load_apps():
    try:
        return json.loads(Path("apps.json").read_text(encoding="utf-8")).get("apps", [])
    except Exception:
        return []

APPS = _load_apps()

def extract_app(text: str) -> dict|None:
    t = (text or "").lower()
    for app in APPS:
        if (app.get("name") or "").lower() in t:
            return app
        for a in app.get("aliases", []):
            if a and a.lower() in t:
                return app
    return None

TRIGGERS = ("ابحث", "بحث", "دوّر", "دور", "سوي بحث", "فتش", "فتّش", "يوتيوب", "ويكيبيديا", "قوقل", "غوغل")

def extract_query(text: str) -> str:
    t = (text or "").strip()
    # خذ ما بعد أول trigger
    first = None
    for tr in TRIGGERS:
        i = t.find(tr)
        if i != -1:
            first = (i, tr)
            break
    if first is None:
        # لو ما في trigger، رجّع النص نفسه (سيتنظف لاحقاً)
        q = t
    else:
        i, tr = first
        q = t[i + len(tr):].strip()

    parts = q.split()
    # احذف كلمات الوقف من البداية
    while parts and parts[0] in STOP:
        parts.pop(0)
    return " ".join(parts)
