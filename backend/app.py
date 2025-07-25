import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import datetime

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Set PORT from .env or default to 10000
PORT = int(os.getenv("PORT", 10000))

# In-memory store for messages
messages = []

# ✅ Root route (important for Render)
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Echo-Me Backend is running!"}), 200

@app.route('/send', methods=['POST'])
def send_message():
    data = request.get_json()

    # Basic validation
    required_fields = ["to", "from", "content", "unlock_date"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    message = {
        "to": data["to"],
        "from": data["from"],
        "content": data["content"],
        "unlock_date": data["unlock_date"]
    }
    messages.append(message)
    return jsonify({"status": "Message scheduled successfully!"}), 200

@app.route('/view', methods=['GET'])
def view_messages():
    today = datetime.date.today().isoformat()

    # Filter messages based on unlock date
    unlocked = [msg for msg in messages if msg['unlock_date'] <= today]
    return jsonify(unlocked), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
