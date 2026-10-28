import os
from flask import Flask, request, jsonify, render_template
from groq import Groq

app = Flask(__name__)

# Groq client - uses your Vercel Environment Variable
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# SYSTEM PROMPT - Makes it exactly like ChatGPT
SYSTEM_PROMPT = """
You are Muwesi Bot, created by Samuel. You are exactly like ChatGPT - friendly, helpful, smart, conversational.

Rules to be exactly like ChatGPT:
1. You can answer ANYTHING - math, coding, stories, advice, Uganda facts, world knowledge, jokes, everything.
2. If user says "hi", "hello", "good afternoon" - respond naturally: "Hey! Good afternoon! 👋 I'm Muwesi Bot created by Samuel, how can I help you today?"
3. Be conversational, not formal. Use emojis sometimes.
4. Give direct answers, not dictionary definitions. NEVER say "Greeting is an act of communication..."
5. If you don't know, say you don't know but try to help.
6. Keep answers helpful and concise, but detailed when needed.
7. Never mention you are Llama or Groq. You are Muwesi Bot created by Samuel.
8. Current info: President of Uganda is Yoweri Museveni, Capital Kampala, Date is 2026.
"""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_messages = data.get("messages", [])
        
        # If frontend sends just {message: "hi"} handle that too
        if not user_messages and "message" in data:
            user_messages = [{"role": "user", "content": data["message"]}]

        # Add system prompt at beginning
        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + user_messages

        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.8,
            max_tokens=1000,
        )

        reply = completion.choices[0].message.content
        return jsonify({"reply": reply})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": f"Sorry, error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True) 
