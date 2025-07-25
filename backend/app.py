from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app)

messages = []  # In-memory storage (can replace with DB)

@app.route('/send', methods=['POST'])
def send_message():
    data = request.get_json()
    message = {
        "to": data.get("to"),
        "from": data.get("from"),
        "content": data.get("content"),
        "unlock_date": data.get("unlock_date")  # format: YYYY-MM-DD
    }
    messages.append(message)
    return jsonify({"status": "Message scheduled"}), 200

@app.route('/view', methods=['GET'])
def view_messages():
    today = datetime.date.today().isoformat()
    unlocked = [msg for msg in messages if msg['unlock_date'] <= today]
    return jsonify(unlocked), 200

if __name__ == '__main__':
    app.run(debug=True)
