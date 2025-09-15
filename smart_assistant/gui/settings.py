from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QFileDialog, QMessageBox)
import json
from pathlib import Path
APPS_PATH = Path("apps.json")

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent); self.setWindowTitle("تعديل التطبيقات"); self.resize(720, 400)
        self.table = QTableWidget(0,6)
        self.table.setHorizontalHeaderLabels(["name","aliases(comma)","windows","linux","darwin","url"])
        btn_add, btn_remove, btn_save = QPushButton("إضافة"), QPushButton("حذف"), QPushButton("حفظ")
        top=QHBoxLayout(); [top.addWidget(b) for b in (btn_add,btn_remove,btn_save)]
        root=QVBoxLayout(self); root.addLayout(top); root.addWidget(self.table)
        btn_add.clicked.connect(self.add_row); btn_remove.clicked.connect(self.remove_selected); btn_save.clicked.connect(self.save)
        self.load()

    def load(self): 
        try: data=json.loads(APPS_PATH.read_text(encoding="utf-8"))
        except: data={"apps":[]}
        self.populate(data.get("apps",[]))

    def save(self):
        apps=[]; 
        for r in range(self.table.rowCount()):
            get=lambda c:(self.table.item(r,c).text().strip() if self.table.item(r,c) else "")
            apps.append({"name":get(0),"aliases":[a.strip() for a in get(1).split(",") if a.strip()],
                         "windows":get(2) or None,"linux":get(3) or None,"darwin":get(4) or None,"url":get(5) or None})
        APPS_PATH.write_text(json.dumps({"apps":apps},ensure_ascii=False,indent=2),encoding="utf-8"); QMessageBox.information(self,"حفظ","تم")

    def populate(self,apps): self.table.setRowCount(0); [self.add_row(a) for a in apps]
    def add_row(self,app=None): r=self.table.rowCount(); self.table.insertRow(r)
        # simplified fill
    def remove_selected(self): [self.table.removeRow(i.row()) for i in self.table.selectedIndexes()]
