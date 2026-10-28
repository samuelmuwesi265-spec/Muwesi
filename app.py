from flask import Flask, render_template, request, jsonify
import os, requests

# === PUT YOUR GROQ KEY HERE === 
# Replace inside quotes with your real gsk_... key
GROQ_API_KEY = "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"
# ==============================

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def get_real_answer(question):
    try:
        q = question.lower().replace("what is","").replace("define","").replace("?","").strip()
        if len(q) < 2:
            q = question
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{q}"
        r = requests.get(url, timeout=5, headers={"User-Agent":"MuwesiBot"})
        if r.status_code == 200:
            data = r.json()
            extract = data.get("extract")
            if extract:
                return extract
    except:
        pass
    return None

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    user_msg = data.get('message','') or ''
    if not user_msg and 'messages' in data:
        msgs = data['messages']
        if msgs:
            last = msgs[-1]
            user_msg = last.get('content','') if isinstance(last, dict) else str(last)

    lower = user_msg.lower()
    reply = None

    # Try Groq AI first (this is your smart ChatGPT)
    try:
        from openai import OpenAI
        # Use the key from top of file
        if GROQ_API_KEY and "PASTE" not in GROQ_API_KEY:
            client = OpenAI(api_key=GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")
            res = client.chat.completions.create(
                model="llama-3.1-8b-instant", # fast, no meandering
                messages=[
                    {"role": "system", "content": "You are Muwesi Bot by Samuel Muwesi from Uganda. Be direct, brief, correct. Max 3-4 sentences. No fluff."},
                    {"role": "user", "content": user_msg}
                ],
                temperature=0.3,
                max_tokens=350
            )
            reply = res.choices[0].message.content
            return jsonify({"reply": reply, "response": reply})
    except Exception as e:
        print(f"Groq error: {e}")

    # If Groq fails, use your old smart logic
    if "what is a computer" in lower or lower.strip() == "computer":
        reply = "A computer is an electronic device that takes data (input), processes it, stores it, and gives results (output). \n\nExamples: Laptop, phone, tablet.\n\nMain parts: 1) Hardware (keyboard, screen, CPU), 2) Software (Windows, apps)."
    elif "biology" in lower:
        reply = "Biology is the study of living things. It studies how plants, animals, and humans live, grow, and reproduce."
    elif "business administration" in lower:
        reply = "Business Administration is managing a business well to make profit. 4 main jobs: 1) Planning, 2) Organizing, 3) Leading, 4) Controlling."
    else:
        wiki = get_real_answer(user_msg)
        if wiki:
            reply = wiki
        else:
            reply = f"Here's a real explanation for '{user_msg}': {user_msg} is important in daily life and education. Ask like 'Explain {user_msg} in detail' for more."

    return jsonify({"reply": reply, "response": reply})

if __name__ == '__main__':
    app.run(debug=True)

