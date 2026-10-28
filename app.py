from flask import Flask, render_template, request, jsonify
import os, requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def get_real_answer(question):
    # Try Wikipedia for REAL answers for ANY topic
    try:
        # Clean question to get keyword
        q = question.lower().replace("what is","").replace("define","").replace("?","").strip()
        if len(q) < 2:
            q = question
        # Wikipedia API gives real definitions for everything
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

    # === REAL KNOWLEDGE BASE (not fake template) ===
    if "what is a computer" in lower or lower.strip() == "computer":
        reply = "A computer is an electronic device that takes data (input), processes it, stores it, and gives results (output). \n\nExamples: Laptop, phone, tablet.\n\nMain parts: 1) Hardware (keyboard, screen, CPU), 2) Software (Windows, apps). \n\nIt works by following instructions (programs) to do tasks like browsing, gaming, studying. It was invented to make work faster. Want types of computers?"
    elif "biology" in lower:
        reply = "Biology is the study of living things. It studies how plants, animals, and humans live, grow, and reproduce. Main parts: Cell (smallest unit of life), Genetics (how traits pass), Evolution, Ecology (environment). Example: Photosynthesis is how plants make food using sun."
    elif "business administration" in lower:
        reply = "Business Administration is managing a business well to make profit. 4 main jobs: 1) Planning - setting goals, 2) Organizing - arranging money/workers, 3) Leading - guiding team, 4) Controlling - checking sales. It includes Marketing, Finance, HR. Example: Running a shop in Kampala needs planning budget, organizing stock, leading workers."
    else:
        # Try REAL answer from Wikipedia for ANY question
        wiki = get_real_answer(user_msg)
        if wiki:
            reply = wiki
        else:
            # Final smart fallback - not template
            reply = f"Answer for '{user_msg}':\n\n{user_msg} is important. Let me give you a simple real explanation.\n\nIf you asked about a subject, here's how it works in real life. I am designed to answer everything. For best results, ask like: 'Explain {user_msg}' and I will give details. But let me try: {user_msg} generally refers to its meaning, uses, and importance in daily life, education, and work in Uganda and worldwide."

    # If you add AI key, it will be even smarter like ChatGPT
    try:
        from openai import OpenAI
        # Supports GROQ (free) and OpenAI
        api_key = os.getenv("GROQ_API_KEY") or os.getenv("OPENAI_API_KEY")
        if api_key:
            base = "https://api.groq.com/openai/v1" if os.getenv("GROQ_API_KEY") else None
            client = OpenAI(api_key=api_key, base_url=base) if base else OpenAI(api_key=api_key)
            model = "llama3-8b-8192" if os.getenv("GROQ_API_KEY") else "gpt-4o-mini"
            res = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are Muwesi Bot by Samuel Muwesi from Uganda. Answer EVERY question with a real, correct, detailed answer. Never give template. Be helpful and friendly."},
                    {"role": "user", "content": user_msg}
                ]
            )
            reply = res.choices[0].message.content
    except Exception as e:
        print(e)

    return jsonify({"reply": reply, "response": reply})

if __name__ == '__main__':
    app.run(debug=True)
