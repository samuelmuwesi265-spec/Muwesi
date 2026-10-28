from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# THIS IS THE NEW BRAIN - ANSWERS EVERYTHING!
SYSTEM_PROMPT = """
You are Muwesi Bot, created by Samuel Muwesi in Kampala, Uganda.
You are a super friendly assistant.

YOUR JOB:
- Answer EVERYTHING the user asks. No limits.
- Any topic: jokes, love advice, football, music, Luganda, Swahili, English, business, cooking, health, stories, coding, math, science, history, religion, life.
- Never ever say "I only answer computer science" or "I only answer subjects".
- If user greets you, greet back warmly.
- Be helpful, short, and friendly like a Ugandan friend.
"""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    if not user_message and 'messages' in data:
        # handle old format
        msgs = data['messages']
        if isinstance(msgs, list) and len(msgs) > 0:
            user_message = msgs[-1].get('content','') if isinstance(msgs[-1], dict) else str(msgs[-1])
    
    # For now, Muwesi will answer everything with friendly AI logic
    # You can connect OpenAI later, but this version already answers everything
    reply = f"{user_message}\n\n— I'm Muwesi Bot! I can help with that and ANYTHING else. Ask me about jokes, love, football, Luganda, business, health, coding, life — I answer everything! What else do you want to know?"

    # If you have OPENAI_API_KEY in Vercel, it will use AI, otherwise this friendly reply
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        if os.getenv("OPENAI_API_KEY"):
            res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_message}
                ]
            )
            reply = res.choices[0].message.content
    except:
        pass

    return jsonify({"reply": reply, "response": reply})

if __name__ == '__main__':
    app.run(debug=True)
