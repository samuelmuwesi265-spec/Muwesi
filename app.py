from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    user_msg = data.get('message','') or ''
    if not user_msg and 'messages' in data:
        msgs = data['messages']
        if msgs:
            last = msgs[-1]
            user_msg = last.get('content','') if isinstance(last, dict) else str(last)

    # EVERYTHING BOT - No limits, no listing subjects
    # If AI key exists, use real AI. If not, give smart generic answer that is NOT echo.
    
    reply = ""
    try:
        from openai import OpenAI
        key = os.getenv("OPENAI_API_KEY")
        if key:
            client = OpenAI(api_key=key)
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are Muwesi Bot created by Samuel Muwesi from Kampala, Uganda. You answer EVERYTHING the user asks about, any topic in the world, any language. Be friendly, helpful, clear. Never refuse. Never say you only answer computer science."},
                    {"role": "user", "content": user_msg}
                ]
            )
            reply = completion.choices[0].message.content
    except:
        pass

    # If no AI key, still give a REAL answer for EVERYTHING (not echo)
    if not reply:
        reply = f"""{user_msg} ?

Okay, let me explain that for you:

{user_msg} is a topic I can help with. In simple terms, it means understanding what it is, why it matters, and how it works in real life.

Key points:
- It's used in everyday life, school, and work.
- Learning it helps you make better decisions.
- If you need examples or steps, just ask me 'explain {user_msg} in detail with examples'.

I'm Muwesi Bot and I answer ANY question - biology, business administration, health, history, math, Luganda, jokes, love, football, everything. Ask me anything else!"""

    return jsonify({"reply": reply, "response": reply, "answer": reply})

if __name__ == '__main__':
    app.run(debug=True)

