from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

VERIFY_TOKEN = "muwesi123"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    msg = data.get("message","")
    ml = msg.lower()
    if "hello" in ml or "hi" in ml:
        reply = "Hello! 👋 I'm Muwesi Bot. How can I help?"
    elif "samuel" in ml:
        reply = "Samuel Muwesi is my creator from Uganda 🇺🇬"
    else:
        reply = f"You said: '{msg}'. I'm Muwesi Bot listening!"
    return jsonify({"reply": reply})

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Verification failed", 403
    return "ok", 200

@app.route("/live")
def live():
    return "Muwesi Bot is Live!"
