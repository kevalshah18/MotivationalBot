import os
import random
import requests
import sys

def get_quote():
    try:
        r = requests.get("https://zenquotes.io/api/random", timeout=8)
        if r.ok:
            data = r.json()
            return f"{data[0]['q']} — {data[0]['a']}"
    except Exception as e:
        print(f"ZenQuotes failed: {e}", file=sys.stderr)

    # Fallback quotes
    fallback = [
        "Discipline beats talent when talent doesn’t show up.",
        "You’re not tired. You’re just uninspired.",
        "Some people dream of success. You're just dreaming. Wake up.",
        "Every day is a new pull request to your future self.",
        "You’re not stuck. You’re just not moving."
    ]
    return random.choice(fallback)

def send_telegram_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    response = requests.post(url, json=payload)
    print("Status:", response.status_code)
    print("Response:", response.text)

if __name__ == "__main__":
    token = os.environ.get("TG_BOT_TOKEN")
    chat_id = os.environ.get("TG_CHAT_ID")

    if not token or not chat_id:
        print("Missing Telegram token or chat ID")
        sys.exit(1)

    message = get_quote()
    send_telegram_message(token, chat_id, message)
