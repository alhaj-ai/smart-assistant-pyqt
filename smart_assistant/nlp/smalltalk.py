# smart_assistant/nlp/smalltalk.py
from __future__ import annotations
import re
import random

# كلمات/أنماط للترحيب، الشكر، الوداع، والأسئلة العامة
GREET_WORDS = {
    "سلام", "السلام", "السلام عليكم", "مرحبا", "اهلا", "هلا", "هلا وسهلا",
    "صباح الخير", "مساء الخير", "مرحباا", "مرحب", "يا هلا"
}
THANKS_WORDS = {"شكرا", "مشكور", "تسلم", "يعطيك العافيه", "ثانكس", "شكرن"}
BYE_WORDS = {"مع السلامه", "الى اللقاء", "في امان الله", "وداعا", "نشوفك"}
QUESTION_WORDS = {
    "كيف", "ليش", "لماذا", "متى", "وين", "اين", "أين", "هل", "كم", "شنو", "شو", "ايش", "ايش؟", "شلون"
}

AR_PUNCT_Q = "؟"   # علامة استفهام عربية
LATIN_Q = "?"      # علامة استفهام لاتينية

GREET_REPLIES = [
    "وعليكم السلام ورحمة الله وبركاته 👋",
    "هلا وغلا! كيف أقدر أخدمك؟",
    "أهلًا وسهلًا! جاهز أنفّذ أوامرك 😉",
    "مرحبا! تقدر تقول: افتح الوورد | يوتيوب تعلم بايثون | ابحث في ويكيبيديا اليمن"
]

THANKS_REPLIES = [
    "العفو! أي خدمة ثانية؟",
    "تسلم 🤝، لو تبغى أفتح برنامج أو أبحث—قلّي.",
    "الله يعافيك! جاهز لأوامرك."
]

BYE_REPLIES = [
    "في أمان الله 👋",
    "سعيد بخدمتك! إلى اللقاء.",
    "مع السلامة، بانـتظارك وقت ما تحتاج."
]

HELP_SUGGESTIONS = (
    "تقدر تقول مثلًا: «افتح الوورد»، «ابحث في ويكيبيديا اليمن»، "
    "«يوتيوب تعلّم بايثون»، «افتح /path/file.pdf»."
)

def is_greeting(text: str) -> bool:
    t = _norm(text)
    return any(w in t for w in GREET_WORDS)

def is_thanks(text: str) -> bool:
    t = _norm(text)
    return any(w in t for w in THANKS_WORDS)

def is_bye(text: str) -> bool:
    t = _norm(text)
    return any(w in t for w in BYE_WORDS)

def is_question(text: str) -> bool:
    t = _norm(text)
    if AR_PUNCT_Q in text or LATIN_Q in text:
        return True
    return any(t.startswith(w) or f" {w} " in t for w in QUESTION_WORDS)

def _norm(s: str) -> str:
    s = (s or "").strip().lower()
    s = s.replace("أ","ا").replace("إ","ا").replace("آ","ا").replace("ة","ه")
    return s

def reply(text: str) -> str | None:
    """
    يحاول توليد ردود محادثة عامة (ترحيب/شكر/وداع/سؤال عام).
    يعيد None لو ما ينطبق كـ smalltalk.
    """
    t = _norm(text)

    if is_greeting(t):
        return random.choice(GREET_REPLIES)

    if is_thanks(t):
        return random.choice(THANKS_REPLIES)

    if is_bye(t):
        return random.choice(BYE_REPLIES)

    if is_question(t):
        # رد عام للأسئلة غير التنفيذية، مع عرض أمثلة
        return (
            "سؤال ممتاز! لو تبغاني أنفّذ شيء على الكمبيوتر قلّي بصيغة أمر.\n"
            f"مثال: {HELP_SUGGESTIONS}"
        )

    # كلمات قصيرة جدًا (سلام، هلا، تمام، او حرف/ايموجي) → نعتبرها smalltalk
    short = t.strip()
    if len(short) <= 2:
        return f"هلا! {HELP_SUGGESTIONS}"

    return None
