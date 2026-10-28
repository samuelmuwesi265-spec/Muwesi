from flask import Flask, request, jsonify, render_template
app = Flask(__name__)
VERIFY_TOKEN = "muwesi123"

# Knowledge base
KNOWLEDGE = {
 "computer science": "Computer Science is the study of computers & computation! It includes: 1) Algorithms & Data Structures 2) Programming Languages 3) AI & Machine Learning 4) Databases 5) Networks 6) Cybersecurity. It's about solving problems using computers. Want to learn programming, algorithms, or AI?",
 "programming": "Programming is giving instructions to computers! Popular languages: Python (easy, for AI), JavaScript (for websites), Java (for apps), C++ (fast). Start with Python - it's best for beginners! Want a roadmap?",
 "algorithm": "An algorithm is step-by-step instructions to solve a problem, like a recipe! Example: Sorting algorithms (Bubble Sort, Quick Sort), Search algorithms. Key is efficiency - Big O notation.",
 "ai": "Artificial Intelligence is making computers think like humans! Includes Machine Learning, Deep Learning, ChatGPT, Computer Vision. AI is the future - built with Python, TensorFlow, PyTorch.",
 "python": "Python is the #1 language in 2026! Easy to learn, powerful for AI, web (Flask/Django), data science. Example: print('Hello Muwesi') . Want to learn Python?",
 "what is": "I'm Muwesi Bot, created by Samuel Muwesi from Uganda! I can explain Computer Science, Programming, AI, and more. Ask me anything specific!"
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    msg = data.get("message","")
    ml = msg.lower()
    
    # Smart search
    reply = None
    for key in KNOWLEDGE:
        if key in ml:
            reply = KNOWLEDGE[key]
            break
    
    if not reply:
        if "hello" in ml or "hi" in ml or "morning" in ml:
            reply = "Hello! 👋 I'm Muwesi Bot by Samuel! I can teach Computer Science, Programming, AI, Python, Algorithms. What do you want to learn?"
        elif "who are you" in ml or "your name" in ml:
            reply = "I'm Muwesi Bot! 🤖 Created by Samuel Muwesi from Uganda to help people learn tech. Ask me about CS!"
        else:
            reply = f"Great question about '{msg}'! In CS, that relates to problem-solving with computers. Could you be more specific? Ask about: programming, python, algorithms, AI, computer science basics."
    
    return jsonify({"reply": reply})

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Verification failed", 403
    return "ok", 200
