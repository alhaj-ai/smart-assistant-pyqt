# 📄 محتوى README.md المقترح

````markdown
# 🧠 Smart Assistant – PyQt6

مساعد ذكي نصي (CLI + GUI) يشبه **Siri/Alexa** لكن مبسط بالعربية.  
يفهم أوامرك حتى لو فيها لهجات/أخطاء إملائية، وينفّذ المطلوب مباشرة على جهازك:

- فتح/إغلاق برامج أو ملفات (Word, Excel, PDF, VS Code…)
- بحث Google / Wikipedia (عربي/إنجليزي)
- بحث وتشغيل فيديو من YouTube
- حفظ وإغلاق مستندات (Word/Excel – Windows فقط عبر COM)
- أوامر نظام: إطفاء / إعادة تشغيل (مع تأكيد)

---

## 📦 متطلبات

- Python 3.10+
- المكتبات:
  ```bash
  pip install -r requirements.txt
  ```
````

- على Windows + Microsoft Office:

  ```bash
  pip install pywin32
  ```

---

## ▶️ التشغيل

### واجهة رسومية (PyQt6 GUI)

```bash
python -m smart_assistant.main
```

### سطر أوامر (CLI)

```bash
python -m smart_assistant.cli_main
```

---

## ⚙️ بنية المشروع

```
smart-assistant-pyqt/
├─ README.md
├─ requirements.txt
├─ apps.json                # تعريف التطبيقات/الأزرار
├─ smart_assistant/
│  ├─ main.py               # تشغيل GUI
│  ├─ cli_main.py           # تشغيل CLI
│  ├─ gui/                  # ملفات الواجهة
│  ├─ core/                 # المنطق (Router, Actions, Office integration)
│  └─ nlp/                  # المعالجة اللغوية (Normalize, Intent, ML...)
└─ tests/                   # اختبارات
```

---

## 📝 أمثلة أوامر

### محادثة عامة

- `سلام` → وعليكم السلام 👋
- `كيف حالك؟` → يرد برد لطيف + اقتراحات أوامر

### بحث

- `ابحث محمد` → Google “محمد”
- `ابحث في ويكيبيديا اليمن` → Wikipedia “اليمن”
- `يوتيوب تعلم بايثون` → تشغيل أول فيديو تعليمي

### فتح/إغلاق/حفظ

- `افتح الوورد`
- `افتح /home/user/report.pdf`
- `اغلق وورد`
- `احفظ`

### Word/Excel (ويندوز فقط)

- `احفظ في الوورد`
- `احفظ باسم تقرير.docx في الوورد`
- `اغلق المستند في الوورد`

### أوامر النظام

- `اطفي` → يطلب تأكيد
- `اطفي أكيد` → تنفيذ إيقاف التشغيل
- `اعادة تشغيل أكيد` → تنفيذ إعادة التشغيل

---

## 🛠️ تخصيص

- أضف برامجك في `apps.json` مع **name** و **aliases** ومسارات التشغيل.
- عدّل أو أضف مرادفات في `nlp/intent.py` أو ردود ترحيب في `nlp/smalltalk.py`.
- أضف بيانات تدريب إضافية في `nlp/training_data.yaml` ثم:

  ```bash
  python -m smart_assistant.nlp.train_intents
  ```

---

## ⚠️ ملاحظات

- YouTube: يشغّل أول فيديو باستخدام `pytube`، ولو فشل يفتح صفحة النتائج.
- Word/Excel: يعمل فقط على Windows + Office + pywin32.
- إطفاء/ريستارت: يتطلب أحيانًا صلاحيات أعلى (Linux).

---
