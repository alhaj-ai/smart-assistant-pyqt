# smart_assistant/nlp/intent.py
from rapidfuzz import fuzz

INTENTS = {
    "greet": [
        "السلام عليكم", "السلام", "مرحبا", "اهلا", "هلا",
        "صباح الخير", "مساء الخير", "هلا وسهلا"
    ],
    "chitchat": [
        "كيف حالك", "كيفك", "كيف الحال", "شو الاخبار", "كيف امورك",
        "كيفك اليوم", "شلونك", "ايش الاخبار"
    ],
    "open": ["افتح", "شغل", "فتح"],
    "close": ["اغلق", "قفل", "انهاء"],
    "search_web": ["ابحث", "بحث", "دور", "دوّر", "سوي بحث", "سوّي بحث", "فتش", "فتّش"],
    "search_google": ["ابحث في قوقل", "ابحث في غوغل", "قوقل", "غوغل"],
    "search_wikipedia": ["ابحث في ويكيبيديا", "ويكيبيديا"],
    "search_youtube": ["ابحث في اليوتيوب", "يوتيوب", "شغل فيديو", "تشغيل فيديو", "فيديو"],
    "save": ["احفظ", "حفظ"],
    "sys": ["اطفي", "اطفاء", "اطفاء الجهاز", "اغلاق النظام", "قفل الجهاز",
            "ريستارت", "اعاده تشغيل", "اعادة تشغيل", "عيد تشغيل"]
}

THRESHOLD = 80

def detect_intent(tokens, original_text: str = ""):
    text = (original_text or "").strip().lower()
    text = text.replace("أ","ا").replace("إ","ا").replace("آ","ا").replace("ة","ه")
    if text:
        for intent, phrases in INTENTS.items():
            for p in phrases:
                if p in text:
                    return intent
    for w in tokens:
        for intent, vocab in INTENTS.items():
            try:
                if max(fuzz.ratio(w, v) for v in vocab) >= THRESHOLD:
                    return intent
            except ValueError:
                continue
    return None
