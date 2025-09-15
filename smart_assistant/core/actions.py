import os, subprocess, webbrowser, platform, psutil, re
from urllib.parse import quote_plus

try:
    import pyautogui
except Exception:
    pyautogui = None

SYSTEM = platform.system().lower()

# ---------- تشغيل هدف/روابط ----------
def open_target(target: dict, info: dict | None):
    if not info:
        return "لا يوجد مسار/رابط مناسب لهذا النظام. عدّل apps.json"
    if info.get("type") == "url":
        webbrowser.open(info["value"])
        return f"فتح الرابط: {info['value']}"
    if info.get("type") == "binary":
        path = info["value"]
        try:
            if SYSTEM == "windows":
                os.startfile(path)  # type: ignore[attr-defined]
            elif SYSTEM == "darwin":
                subprocess.Popen(["open", path])
            else:
                subprocess.Popen([path])
            return f"تشغيل: {target.get('name') or path}"
        except Exception as e:
            return f"تعذّر التشغيل: {e}"
    return "نوع هدف غير مدعوم"

def close_app_by_name(app_name: str):
    killed = False
    for proc in psutil.process_iter(["name"]):
        try:
            name = (proc.info.get("name") or "").lower()
        except psutil.Error:
            continue
        if app_name.lower().split()[0] in name:
            try:
                proc.terminate()
                killed = True
            except psutil.AccessDenied:
                pass
    return "تم الإنهاء" if killed else "لم يتم العثور على العملية"

# ---------- البحث ----------
def search_web(query: str):
    if not query:
        webbrowser.open("https://www.google.com"); return "فتح Google"
    webbrowser.open(f"https://www.google.com/search?q={quote_plus(query)}")
    return f"بحث Google: {query}"

def search_google(query: str):
    return search_web(query)

def search_wikipedia(query: str, lang: str = "ar"):
    if not query:
        webbrowser.open(f"https://{lang}.wikipedia.org"); return "فتح ويكيبيديا"
    url = f"https://{lang}.wikipedia.org/wiki/Special:Search?search={quote_plus(query)}"
    webbrowser.open(url); return f"بحث ويكيبيديا: {query}"

YOUTUBE_URL_RE = re.compile(r"(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[^\s]+")

def search_youtube(query: str):
    if not query:
        webbrowser.open("https://www.youtube.com"); return "فتح YouTube"
    if YOUTUBE_URL_RE.search(query):
        url = query if query.startswith("http") else "https://" + query
        webbrowser.open(url); return "تشغيل فيديو YouTube"
    # جرّب تشغيل أول فيديو عبر pytube، وإلا ارجع لنتائج البحث
    try:
        from pytube import Search
        s = Search(query)
        if s.results:
            vid = s.results[0].watch_url
            webbrowser.open(vid)
            return f"تشغيل أول فيديو: {vid}"
    except Exception:
        pass
    webbrowser.open(f"https://www.youtube.com/results?search_query={quote_plus(query)}")
    return f"بحث YouTube: {query}"

# ---------- حفظ ----------
def save_active_document():
    if pyautogui is None:
        return "pyautogui غير مثبت. ثبّته لتفعيل الحفظ الفعلي."
    try:
        if SYSTEM == "darwin":
            pyautogui.hotkey("command", "s")
        else:
            pyautogui.hotkey("ctrl", "s")
        return "تم إرسال اختصار الحفظ (Ctrl/⌘+S)"
    except Exception as e:
        return f"تعذّر إرسال الاختصار: {e}"

# ---------- فتح ملف بالمسار ----------
def open_file_path(path: str):
    path = os.path.expanduser(path)
    if not os.path.exists(path):
        return f"الملف غير موجود: {path}"
    try:
        if SYSTEM == "windows":
            os.startfile(path)  # type: ignore[attr-defined]
        elif SYSTEM == "darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
        return f"فتح الملف: {path}"
    except Exception as e:
        return f"تعذّر فتح الملف: {e}"

# ---------- أوامر نظام مع تأكيد ----------
CONFIRM_WORDS = {"اكيد","أكيد","موافق","نعم","تمام","الحين","الان","الآن","نفذ","نفّذ"}

def _has_confirmation(tokens: list[str]) -> bool:
    txt = " ".join(tokens)
    return any(w in txt for w in CONFIRM_WORDS)

def _exec_shutdown():
    try:
        if SYSTEM == "windows":
            subprocess.Popen(["shutdown", "/s", "/t", "0"]); return "جاري إيقاف التشغيل…"
        elif SYSTEM == "darwin":
            subprocess.Popen(["osascript","-e",'tell application "System Events" to shut down'])
            return "طلب إيقاف تشغيل macOS…"
        else:
            for cmd in (["systemctl","poweroff"],["shutdown","-h","now"]):
                try:
                    subprocess.Popen(cmd); return "جاري إيقاف التشغيل (قد يتطلب صلاحيات)…"
                except Exception:
                    continue
            return "تعذّر إرسال أمر الإيقاف. قد تحتاج sudo."
    except Exception as e:
        return f"تعذّر إيقاف التشغيل: {e}"

def _exec_reboot():
    try:
        if SYSTEM == "windows":
            subprocess.Popen(["shutdown", "/r", "/t", "0"]); return "جاري إعادة التشغيل…"
        elif SYSTEM == "darwin":
            subprocess.Popen(["osascript","-e",'tell application "System Events" to restart'])
            return "طلب إعادة تشغيل macOS…"
        else:
            for cmd in (["systemctl","reboot"],["shutdown","-r","now"]):
                try:
                    subprocess.Popen(cmd); return "جاري إعادة التشغيل (قد يتطلب صلاحيات)…"
                except Exception:
                    continue
            return "تعذّر إرسال أمر إعادة التشغيل. قد تحتاج sudo."
    except Exception as e:
        return f"تعذّر إعادة التشغيل: {e}"

def system_command(tokens):
    txt = " ".join(tokens)
    is_reboot = any(w in txt for w in ["اعاده تشغيل","اعادة تشغيل","عيد تشغيل","ريستارت"])
    is_shutdown = any(w in txt for w in ["اطفي","اطفاء","اطفاء الجهاز","اغلاق النظام","قفل الجهاز"])
    if not (is_shutdown or is_reboot):
        return "أمر نظام غير معروف"
    if not _has_confirmation(tokens):
        return ("⚠️ هذا الأمر سيطفئ الجهاز. للتنفيذ اكتب: «اطفي أكيد» أو «اطفاء الجهاز الآن»."
                if is_shutdown else
                "⚠️ هذا الأمر سيعيد تشغيل الجهاز. للتنفيذ اكتب: «اعادة تشغيل أكيد» أو «ريستارت الآن».")
    return _exec_reboot() if is_reboot else _exec_shutdown()
