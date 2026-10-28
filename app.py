from flask import Flask, request
import requests
import os
from datetime import datetime
import pytz

app = Flask(__name__)

TOKEN = os.environ.get("TOKEN", "")
PHONE_ID = os.environ.get("PHONE_ID", "")
VERIFY_TOKEN = "muwesi123"

KAMPALA_TZ = pytz.timezone("Africa/Kampala")

def get_greeting():
    hour = datetime.now(KAMPALA_TZ).hour
    if 5 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 17:
        return "Good afternoon"
    elif 17 <= hour < 21:
        return "Good evening"
    else:
        return "Hello"

def send_whatsapp(to, text):
    if not TOKEN or not PHONE_ID:
        print("Missing TOKEN/PHONE_ID")
        return
    url = f"https://graph.facebook.com/v19.0/{PHONE_ID}/messages"
    headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
    data = {"messaging_product": "whatsapp", "to": to, "type": "text", "text": {"body": text}}
    try:
        requests.post(url, headers=headers, json=data, timeout=10)
    except Exception as e:
        print(f"Send error: {e}")

@app.route("/", methods=["GET"])
def home():
    return "Muwesi Bot is Live!"

@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Verification failed", 403

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    try:
        entry = data["entry"][0]
        change = entry["changes"][0]
        value = change["value"]
        if "messages" in value:
            msg = value["messages"][0]
            from_number = msg["from"]
            text_body = msg.get("text", {}).get("body", "").lower().strip()
            greeting = get_greeting()

            if text_body in ["hi", "hello", "hey", "hlo", "olyo"]:
                reply = f"{greeting}! 👋\nI am Muwesi Sports Bot.\n\nSend:\n* tips - for betting tips\n* news - for sports news\n* scores - for live scores\n* help"
            elif "tips" in text_body or "tip" in text_body:
                reply = f"{greeting}! ⚽🔥 *Today's Top Tips:*\n\n1. Man City vs Arsenal - Over 1.5 Goals ✅\n2. Real Madrid Win\n3. Barca - BTTS Yes\n4. Al Ahly - Under 3.5\n\n_18+ Gamble Responsibly_"
            elif "news" in text_body:
                reply = "📰 *Sports News Update*\n\n• Premier League: Title race heats up!\n• UPL: Vipers SC leads table\n• Champions League returns this week\n\nSend *scores* for live results."
            elif "score" in text_body:
                reply = "⚽ *Live Scores*\n\nMan Utd 2-1 Liverpool (78')\nArsenal 0-0 Chelsea (HT)\nVipers 1-0 KCCA (Live)\n\nMore updates soon!"
            elif "help" in text_body:
                reply = "🤖 *Muwesi Bot Help*\n\nCommands:\n- hi / hello\n- tips\n- news\n- scores\n- help"
            else:
                reply = f"{greeting}! I got: '{text_body}'\n\nTry sending *tips* or *news* or *scores*"

            send_whatsapp(from_number, reply)
    except Exception as e:
        print(f"Webhook error: {e}")
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
