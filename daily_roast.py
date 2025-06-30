
#!/usr/bin/env python3
"""
Daily Telegram Roast / Motivation Bot
"""

import os
import random
from datetime import datetime, timezone, timedelta
import requests

BOT_TOKEN = "7832751743:AAEGs4AHSblub_J5EhXcIN4VB39502W4jkE"
CHAT_ID   = "5278116390"

SEND_HOUR   = 6
SEND_MINUTE = 30

ROASTS = [
    "Your goals are waiting. Don’t let time win by default.",
    "Every line of code today brings you closer to your dream role.",
    "Discipline beats talent when talent doesn’t show up.",
    "Even the best roadmap means nothing without action.",
    "FAANG‑level prep needs FAANG‑level focus — stay locked in.",
    "Success doesn’t come from wishing — it comes from doing.",
    "Stay consistent. You don’t rise by motivation — you rise by habit.",
    "One task done well beats ten half‑finished plans.",
    "Grind quietly. Let results talk louder than words.",
    "Your time is your capital — invest it in skills, not scrolling.",
    "Momentum is your secret weapon. Don’t break the chain.",
    "Smart work compounds. One hour a day beats zero every time.",
    "Six months of discipline can rewrite your next six years.",
    "The job you want is already hiring — be the one they notice.",
    "Every small step you take now is a loud win in disguise.",
    "You already know what to do. So do it, with no drama.",
    "Focus on code, clarity, and consistency — results will follow.",
    "Small progress daily beats big promises rarely.",
    "You're not late; you're one deep session away from momentum.",
    "Work like someone out there is preparing harder."
]

def ist_now():
    return datetime.now(timezone(timedelta(hours=5, minutes=30)))

def should_send_now(h, m):
    now = ist_now()
    return now.hour == h and now.minute == m

def build_message():
    line = random.choice(ROASTS)
    timestamp = ist_now().strftime("%Y-%m-%d %H:%M")
    return f"📣 {line}\n🗓 {timestamp}"

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': text}
    try:
        requests.post(url, data=payload, timeout=10).raise_for_status()
    except requests.RequestException as exc:
        print("Telegram send failed:", exc)

def main():
    if 'FORCE_SEND' in os.environ or should_send_now(SEND_HOUR, SEND_MINUTE):
        send_message(build_message())

if __name__ == "__main__":
    main()
