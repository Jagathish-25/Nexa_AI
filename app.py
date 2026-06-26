from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import requests
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# API KEY (from .env file)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# System instruction
SYSTEM_PROMPT = """
You are Nexa AI, a professional AI assistant.

Rules:
- No greetings like "nice to meet you"
- No filler sentences
- Keep answers short and clear
- Be direct and useful
"""

# ✅ HOME ROUTE (fixes "URL not found")
@app.route("/")
def home():
    return jsonify({
        "message": "Nexa AI backend is running 🚀"
    })


# ✅ CHAT ROUTE
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()

        if not data or "message" not in data:
            return jsonify({"reply": "Invalid request"}), 400

        user_message = data["message"]

        # Call Groq API
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_message}
                ]
            },
            timeout=30
        )

        # If API fails
        if response.status_code != 200:
            return jsonify({
                "reply": "AI service busy. Try again later."
            }), 500

        result = response.json()

        reply = result["choices"][0]["message"]["content"]

        return jsonify({
            "reply": reply.strip()
        })

    except Exception as e:
        return jsonify({
            "reply": "Server error",
            "error": str(e)
        }), 500


# Run locally
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)