import platform
if platform.system().lower() != "windows":
    raise ImportError("office_win works only on Windows.")

import win32com.client as win32
from pathlib import Path

# -------- Word --------
def word_open(doc_path: str|Path):
    word = win32.gencache.EnsureDispatch("Word.Application")
    word.Visible = True
    return word.Documents.Open(str(Path(doc_path)))

def word_save_active():
    word = win32.gencache.EnsureDispatch("Word.Application")
    doc = word.ActiveDocument
    doc.Save()
    return "تم حفظ المستند الحالي في Word"

def word_save_as(doc_path: str|Path):
    word = win32.gencache.EnsureDispatch("Word.Application")
    doc = word.ActiveDocument
    doc.SaveAs(str(Path(doc_path)))
    return f"تم الحفظ باسم: {doc_path}"

def word_close_active(save_changes=True):
    word = win32.gencache.EnsureDispatch("Word.Application")
    doc = word.ActiveDocument
    doc.Close(SaveChanges=save_changes)
    return "تم إغلاق المستند الحالي في Word"

# -------- Excel --------
def excel_open(xl_path: str|Path):
    xl = win32.gencache.EnsureDispatch("Excel.Application")
    xl.Visible = True
    return xl.Workbooks.Open(str(Path(xl_path)))

def excel_save_active():
    xl = win32.gencache.EnsureDispatch("Excel.Application")
    wb = xl.ActiveWorkbook
    wb.Save()
    return "تم حفظ المصنف الحالي في Excel"

def excel_save_as(xl_path: str|Path):
    xl = win32.gencache.EnsureDispatch("Excel.Application")
    wb = xl.ActiveWorkbook
    wb.SaveAs(str(Path(xl_path)))
    return f"تم الحفظ باسم: {xl_path}"

def excel_close_active(save_changes=True):
    xl = win32.gencache.EnsureDispatch("Excel.Application")
    wb = xl.ActiveWorkbook
    wb.Close(SaveChanges=save_changes)
    return "تم إغلاق المصنف الحالي في Excel"
