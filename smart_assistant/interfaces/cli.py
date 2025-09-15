from smart_assistant.core.router import route
from smart_assistant.core.history import History

def run_cli():
    print("Smart Assistant CLI – اكتب أمرًا (خروج لإنهاء):")
    hist = History()
    while True:
        try:
            t = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nمع السلامة")
            break
        if not t:
            continue
        if t in {"خروج", "exit", "quit"}:
            print("مع السلامة")
            break
        print(route(t, hist))
