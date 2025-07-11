from flask import Flask, request, jsonify
import africastalking
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

username = os.getenv("AFRICASTALKING_USERNAME")
api_key = os.getenv("AFRICASTALKING_API_KEY")
africastalking.initialize(username, api_key)
sms = africastalking.SMS

API_SECRET_KEY = os.getenv("API_SECRET_KEY")  

@app.route("/")
def home():
    return "Albinism Konnect API running powered by Africa's Talking!"

@app.route("/send-sms", methods=["POST"])
def send_sms():
    client_key = request.headers.get("x-api-key")
    if client_key != API_SECRET_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    to = data.get("to")
    message = data.get("message")

    if not to or not message:
        return jsonify({"error": "Missing 'to' or 'message'"}), 400

    try:
        # Accept both a single number (string) or list of numbers
        if isinstance(to, str):
            recipients = [to]
        elif isinstance(to, list):
            recipients = to
        else:
            return jsonify({"error": "'to' must be a string or list of strings"}), 400

        response = sms.send(message, recipients)
        return jsonify({"status": "success", "response": response})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
