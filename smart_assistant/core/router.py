# smart_assistant/core/router.py
import re, platform
from smart_assistant.nlp.normalizer import normalize
from smart_assistant.nlp.tokenizer import tokenize
from smart_assistant.nlp.intent import detect_intent
from smart_assistant.nlp.intent_ml import ml_predict_intent
from smart_assistant.nlp.ner_rules import extract_app, extract_query
from smart_assistant.nlp.smalltalk import reply as smalltalk_reply
from smart_assistant.nlp.target import find_target, resolve_launch_info
from smart_assistant.core.actions import (
    open_target, close_app_by_name, search_web, save_active_document,
    system_command, open_file_path, search_google, search_wikipedia, search_youtube
)

IS_WIN = platform.system().lower() == "windows"
if IS_WIN:
    try:
        from smart_assistant.core.office_win import (
            word_open, word_save_active, word_save_as, word_close_active,
            excel_open, excel_save_active, excel_save_as, excel_close_active
        )
    except Exception:
        word_open = word_save_active = word_save_as = word_close_active = None
        excel_open = excel_save_active = excel_save_as = excel_close_active = None

PATH_RE = re.compile(r'(?:/[^\s]+|[a-zA-Z]:\\[^\s]+)')
FILE_EXTS = (".pdf",".docx",".doc",".xlsx",".xls",".pptx",".txt",".png",".jpg",".jpeg",".mp4",".mp3")
CHAIN_SPLIT = re.compile(r"\s*(?:ثم|وبعدين|بعدها|بعدين|ومن ثم|وثم|و بعدين)\s*", re.IGNORECASE)

def _route_single(raw_text: str, history):
    # أولاً: ردود محادثة عامة (ترحيب/سؤال/شكر/وداع/قصير جدًا)
    st = smalltalk_reply(raw_text)
    if st is not None:
        history.add_entry(raw=raw_text, normalized=normalize(raw_text), intent="smalltalk", target=None)
        return st

    clean = normalize(raw_text)
    tokens = tokenize(clean)

    # 1) ملف/مسار صريح
    m = PATH_RE.search(raw_text)
    if m and any(m.group(0).lower().endswith(ext) for ext in FILE_EXTS):
        history.add_entry(raw=raw_text, normalized=clean, intent="open_file", target=m.group(0))
        return open_file_path(m.group(0))

    # 2) ML أولاً (دلالي)، ثم القواعد كاحتياط
    ml_intent, conf = ml_predict_intent(clean)
    rule_intent = detect_intent(tokens, original_text=clean)
    intent = ml_intent if conf >= 0.55 else rule_intent

    # 3) الهدف/الكيانات
    app = extract_app(clean) or find_target(tokens)
    query = extract_query(raw_text)

    history.add_entry(raw=raw_text, normalized=clean, intent=intent, target=app or query)

    # 4) تنفيذ أساسي
    if intent in {"open_app", "open"} and app:
        info = resolve_launch_info(app); return open_target(app, info)
    if intent in {"close_app","close"} and app:
        return close_app_by_name(app.get("name"))
    if intent in {"save_doc","save"}:
        return save_active_document()
    if intent in {"search_youtube"}:
        return search_youtube(query)
    if intent in {"search_wikipedia"}:
        return search_wikipedia(query, lang="ar")
    if intent in {"search_google","search_web"}:
        return search_google(query)
    if intent in {"sys_shutdown","sys_reboot","sys"}:
        return system_command(tokens)

    # 5) قواعد Windows Word/Excel (اختيارية)
    t = clean
    if IS_WIN:
        # Word
        if ("وورد" in t or "word" in t) and any([word_save_active, word_save_as, word_close_active, word_open]):
            if "احفظ باسم" in t or "حفظ باسم" in t:
                name = t.split("باسم",1)[1].strip() if "باسم" in t else ""
                name = name or "document1.docx"
                return word_save_as(name) if word_save_as else "ميزة Word SaveAs غير متاحة"
            if "احفظ" in t or "حفظ" in t:
                return word_save_active() if word_save_active else "ميزة Word Save غير متاحة"
            if "اغلق" in t or "اقفل" in t or "انهاء" in t:
                return word_close_active() if word_close_active else "ميزة Word Close غير متاحة"
            if "افتح" in t and PATH_RE.search(raw_text):
                return word_open(PATH_RE.search(raw_text).group(0)) if word_open else "ميزة Word Open غير متاحة"

        # Excel
        if ("اكسل" in t or "excel" in t) and any([excel_save_active, excel_save_as, excel_close_active, excel_open]):
            if "احفظ باسم" in t or "حفظ باسم" in t:
                name = t.split("باسم",1)[1].strip() if "باسم" in t else ""
                name = name or "workbook1.xlsx"
                return excel_save_as(name) if excel_save_as else "ميزة Excel SaveAs غير متاحة"
            if "احفظ" in t or "حفظ" in t:
                return excel_save_active() if excel_save_active else "ميزة Excel Save غير متاحة"
            if "اغلق" in t or "اقفل" in t or "انهاء" in t:
                return excel_close_active() if excel_close_active else "ميزة Excel Close غير متاحة"
            if "افتح" in t and PATH_RE.search(raw_text):
                return excel_open(PATH_RE.search(raw_text).group(0)) if excel_open else "ميزة Excel Open غير متاحة"

    # 6) fallback: لو تعرّف على تطبيق بدون نية → فتح
    if app:
        info = resolve_launch_info(app); return open_target(app, info)

    # 7) آخر ملاذ
    return "جاهز! تقدر تقول: «افتح الوورد»، «ابحث محمد»، «يوتيوب تعلّم بايثون»، «افتح /path/file.pdf»."

def route(text: str, history):
    parts = [p for p in CHAIN_SPLIT.split(text) if p.strip()]
    if not parts:
        return "لا شيء للتنفيذ."
    results = [ _route_single(p.strip(), history) for p in parts ]
    return "\n".join(results) if len(results) > 1 else results[0]
