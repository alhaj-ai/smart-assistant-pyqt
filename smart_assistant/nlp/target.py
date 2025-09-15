import json
import platform
from rapidfuzz import process

with open("apps.json", "r", encoding="utf-8") as f:
    APPS_DATA = json.load(f).get("apps", [])

ALIASES = {}
for app in APPS_DATA:
    for a in app.get("aliases", []):
        ALIASES[a.lower()] = app

SYSTEM = platform.system().lower()  # 'windows'|'linux'|'darwin'

def find_target(tokens):
    if not ALIASES:
        return None
    text = " ".join(tokens).lower()
    choices = list(ALIASES.keys())
    match = process.extractOne(text, choices)
    if match and match[1] >= 70:
        return ALIASES[match[0]]
    for t in tokens:
        match = process.extractOne(t.lower(), choices)
        if match and match[1] >= 85:
            return ALIASES[match[0]]
    return None

def resolve_launch_info(app):
    if not app:
        return None
    if "url" in app:
        return {"type": "url", "value": app["url"]}
    key = SYSTEM
    path = app.get(key)
    if path:
        return {"type": "binary", "value": path}
    return None
