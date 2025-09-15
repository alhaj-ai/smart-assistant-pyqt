# smart_assistant/gui/main_window.py
from __future__ import annotations

import json
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTextEdit, QListWidget, QListWidgetItem,
    QMenuBar, QStatusBar, QScrollArea, QFrame, QSizePolicy
)

from smart_assistant.core.router import route
from smart_assistant.core.history import History
from smart_assistant.core.actions import open_target
from smart_assistant.gui.settings import SettingsDialog
from smart_assistant.nlp.target import resolve_launch_info


APPS_JSON = Path("apps.json")


class MainWindow(QMainWindow):
    """
    واجهة PyQt6:
    - شريط أزرار Launcher يُحمِّل البرامج من apps.json
    - إدخال أوامر نصية + تنفيذ/حفظ
    - مخرجات وسجل History
    - قائمة إعدادات لتعديل apps.json
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Assistant – PyQt6")
        self.resize(1000, 680)

        self.history = History()

        # ======= القائمة =======
        menubar = QMenuBar(self)
        self.setMenuBar(menubar)
        settings_menu = menubar.addMenu("إعدادات")
        act_open_settings = settings_menu.addAction("تعديل التطبيقات…")
        act_open_settings.triggered.connect(self.open_settings)

        # ======= عناصر الإدخال =======
        self.input = QLineEdit()
        self.input.setPlaceholderText(
            "اكتب أمرك… مثال: افتح الوورد | ابحث الذكاء الاصطناعي | افتح /path/file.pdf"
        )
        self.run_btn = QPushButton("تنفيذ")
        self.save_btn = QPushButton("حفظ (Ctrl/⌘+S)")

        # ======= المخرجات والسجل =======
        self.output = QTextEdit(readOnly=True)
        self.output.setPlaceholderText("النتائج تظهر هنا…")

        self.history_list = QListWidget()
        self.history_list.setMinimumWidth(280)

        # ======= شريط أزرار التطبيقات (Launcher) =======
        self.launcher_layout = QHBoxLayout()
        self.launcher_layout.setSpacing(8)

        bar_widget = QWidget()
        bar_widget.setLayout(self.launcher_layout)

        bar_scroll = QScrollArea()
        bar_scroll.setWidget(bar_widget)
        bar_scroll.setWidgetResizable(True)
        bar_scroll.setFrameShape(QFrame.Shape.NoFrame)
        bar_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        bar_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        bar_scroll.setFixedHeight(72)

        # تحميل الأزرار من apps.json
        self.load_launcher_buttons()

        # ======= التخطيطات =======
        top = QHBoxLayout()
        top.addWidget(self.input, 1)
        top.addWidget(self.run_btn)
        top.addWidget(self.save_btn)

        center = QHBoxLayout()
        center.addWidget(self.output, 1)
        center.addWidget(self.history_list)

        root = QVBoxLayout()
        root.addWidget(bar_scroll)     # شريط التطبيقات في الأعلى
        root.addLayout(top)
        root.addLayout(center, 1)

        container = QWidget()
        container.setLayout(root)
        self.setCentralWidget(container)

        self.setStatusBar(QStatusBar())

        # ======= الإشارات =======
        self.run_btn.clicked.connect(self.on_run)
        self.save_btn.clicked.connect(self.on_save)
        self.input.returnPressed.connect(self.on_run)
        self.history_list.itemDoubleClicked.connect(self.on_reuse_item)

    # ------------------------------------------------------------------
    #                           Utilities
    # ------------------------------------------------------------------
    def load_launcher_buttons(self):
        """تحميل أزرار التطبيقات من apps.json."""
        self._clear_layout(self.launcher_layout)

        try:
            data = json.loads(APPS_JSON.read_text(encoding="utf-8"))
            apps = data.get("apps", [])
        except Exception:
            apps = []

        if not apps:
            placeholder = QPushButton("لا توجد تطبيقات في apps.json")
            placeholder.setEnabled(False)
            self.launcher_layout.addWidget(placeholder)
        else:
            for app in apps:
                name = app.get("name") or "App"
                btn = QPushButton(name)
                btn.setCursor(Qt.CursorShape.PointingHandCursor)
                btn.clicked.connect(lambda _, a=app: self.launch_app(a))
                self.launcher_layout.addWidget(btn)

        # Spacer يتمدد ليمنع التصاق الأزرار
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.launcher_layout.addWidget(spacer)

    def _clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()

    # ------------------------------------------------------------------
    #                           Actions
    # ------------------------------------------------------------------
    def launch_app(self, app: dict):
        """تشغيل تطبيق من زر Launcher."""
        info = resolve_launch_info(app)
        result = open_target(app, info)
        self.output.append(f"→ {app.get('name', 'App')}")
        self.output.append(f"← {result}\n")
        self.statusBar().showMessage(result, 2500)

    def on_run(self):
        """تنفيذ الأمر النصي عبر بايبلاين المساعد."""
        text = self.input.text().strip()
        if not text:
            return
        result = route(text, self.history)
        self.output.append(f"→ {text}")
        self.output.append(f"← {result}\n")
        item = QListWidgetItem(text)
        item.setToolTip(result)
        self.history_list.addItem(item)
        self.input.clear()
        self.statusBar().showMessage("تم التنفيذ", 2000)

    def on_save(self):
        """إرسال اختصار الحفظ (Ctrl/⌘+S) للتطبيق النشط."""
        from smart_assistant.core.actions import save_active_document
        msg = save_active_document()
        self.output.append(f"← {msg}\n")
        self.statusBar().showMessage(msg, 2000)

    def on_reuse_item(self, item: QListWidgetItem):
        """إعادة استخدام أمر من السجل إلى خانة الإدخال."""
        self.input.setText(item.text())
        self.input.setFocus()
        self.input.end(False)

    # ------------------------------------------------------------------
    #                           Settings
    # ------------------------------------------------------------------
    def open_settings(self):
        """فتح نافذة إعدادات لإدارة apps.json ثم إعادة تحميل الأزرار."""
        dlg = SettingsDialog(self)
        dlg.exec()  # حفظ من داخل النافذة
        self.load_launcher_buttons()  # إعادة التحميل على أي حال
