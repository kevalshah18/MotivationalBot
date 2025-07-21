import os
import random
import requests
import sys
import time

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # Not required in GitHub Actions

FALLBACK_QUOTES = [
    "Discipline beats talent when talent doesn’t show up.",
    "You’re not tired. You’re just uninspired.",
    "Some people dream of success. You're just dreaming. Wake up.",
    "Every day is a new pull request to your future self.",
    "You’re not stuck. You’re just not moving.",
    "You say you're learning to code — but GitHub says otherwise.",
    "Your motivation left the chat. Maybe open the IDE now?",
    "If consistency is king, you're a court jester.",
    "Your goals aren't unreachable. You just haven’t stood up.",
    "At this rate, the bugs will graduate before you do."
]

CUSTOM_ROASTS = [
    "You're not a procrastinator. You're just aggressively waiting for motivation.",
    "If effort was coffee, you'd still be asleep.",
    "‘Tomorrow’ isn’t a plan. It's an excuse you rehearse daily.",
    "Keep going — or just admit you're not serious.",
    "Your dreams called. They’re filing a restraining order."
]

def get_from_zenquotes():
    try:
        r = requests.get("https://zenquotes.io/api/random", timeout=8)
        r.raise_for_status()
        data = r.json()
        return f"{data[0]['q']} — {data[0]['a']}"
    except Exception as e:
        print(f"[ZenQuotes FAIL] {e}", file=sys.stderr)
        return None

def get_from_theysaidso():
    try:
        r = requests.get("https://quotes.rest/qod?category=inspire", headers={"Accept": "application/json"}, timeout=8)
        r.raise_for_status()
        data = r.json()
        quote = data["contents"]["quotes"][0]
        return f"{quote['quote']} — {quote['author']}"
    except Exception as e:
        print(f"[TheySaidSo FAIL] {e}", file=sys.stderr)
        return None

def get_random_roast():
    sources = [
        get_from_zenquotes,
        get_from_theysaidso,
        lambda: random.choice(CUSTOM_ROASTS),
        lambda: random.choice(FALLBACK_QUOTES)
    ]
    for source in sources:
        quote = source()
        if quote:
            return quote
    return "Still nothing? That's just laziness at this point."

def send_telegram_message(token, chat_id, message, max_retries=3):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            print("[INFO] Message sent successfully")
            return
        except Exception as e:
            print(f"[WARN] Attempt {attempt}: Failed to send message - {e}", file=sys.stderr)
            time.sleep(2)
    print("[ERROR] All attempts to send message failed.", file=sys.stderr)

def main():
    token = os.getenv("TG_BOT_TOKEN")
    chat_id = os.getenv("TG_CHAT_ID")

    if not token or not chat_id:
        print("[ERROR] Missing Telegram credentials", file=sys.stderr)
        sys.exit(1)

    quote = get_random_roast()
    send_telegram_message(token, chat_id, quote)

if __name__ == "__main__":
    main()
