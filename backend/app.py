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

# ✅ Root route (important for Render or Railway)
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Echo-Me Backend is running!"}), 200

# ✅ Send a new scheduled message
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

# ✅ View only unlocked messages (for today or earlier)
@app.route('/view', methods=['GET'])
def view_messages():
    today = datetime.date.today().isoformat()
    unlocked = [msg for msg in messages if msg['unlock_date'] <= today]
    return jsonify(unlocked), 200

# ✅ View all messages (for frontend to split locked/unlocked)
@app.route('/view-all', methods=['GET'])
def view_all_messages():
    return jsonify(messages), 200

# ✅ Start server
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
