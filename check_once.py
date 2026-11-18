import json
import os

import requests

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

PAGES = {
    "VOX Mall of Egypt (elcinema)": "https://elcinema.com/en/theater/3101271",
    "City Stars Cinema (elcinema)": "https://elcinema.com/en/theater/3101050",
    "Golden Stars VIP (elcinema)": "https://elcinema.com/en/theater/3101253",
}

KEYWORDS = ["doomsday", "يوم القيامة", "المنتقمون"]

STATE_FILE = "state.json"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; personal-alert-bot)"}


def send_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    r = requests.post(url, data={"chat_id": CHAT_ID, "text": text}, timeout=20)
    r.raise_for_status()


def load_state():
    try:
        with open(STATE_FILE, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def main():
    if os.environ.get("SEND_TEST") == "true":
        send_telegram("Test OK. The Doomsday alert bot can message you.")

    state = load_state()

    for name, url in PAGES.items():
        if state.get(name):
            continue
        try:
            r = requests.get(url, headers=HEADERS, timeout=30)
            r.raise_for_status()
            text = r.text.lower()
            if any(k.lower() in text for k in KEYWORDS):
                send_telegram(f"Doomsday is now listed at {name}!\n{url}\nGo book now.")
                state[name] = True
        except Exception as e:
            print(f"{name}: {e}")

    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False)


if __name__ == "__main__":
    main()
