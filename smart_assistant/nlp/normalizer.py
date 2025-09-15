import re

def normalize(text: str) -> str:
    # إزالة التشكيل
    text = re.sub(r"[ًٌٍَُِّْ]", "", text)
    # توحيد الحروف
    text = text.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")
    text = text.replace("ة", "ه")
    return text.strip().lower()
