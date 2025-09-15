import json
from pathlib import Path

class History:
    def __init__(self, path: str | Path = ".history.json"):
        self.path = Path(path)
        self.data = []
        if self.path.exists():
            try:
                self.data = json.loads(self.path.read_text(encoding="utf-8"))
            except Exception:
                self.data = []

    def add_entry(self, **entry):
        self.data.append(entry)
        try:
            self.path.write_text(
                json.dumps(self.data, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        except Exception:
            pass
