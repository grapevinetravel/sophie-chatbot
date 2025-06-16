import html
import json

from flask import Flask, request, jsonify
from pydantic import BaseModel
from uuid import uuid4
from gpt.gpt_chat import run_chat
from flask_cors import CORS
app = Flask(__name__)
CORS(app)  # This allows all origins, methods, and headers
conversation_store = {}

class ChatRequest(BaseModel):
    message: str
    conversation_id: str = None

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    print("Chat request:" + str(data))

    if not data or "message" not in data:
        return jsonify({"error": "Missing message"}), 400

    req = ChatRequest(**data)
    conv_id = req.conversation_id or str(uuid4())
    reply = run_chat(req.message, conv_id, conversation_store)
    result = jsonify({"reply": reply, "conversation_id": conv_id})
    print("Chat response:" + str(result))

    return result
@app.route("/login", methods=["POST"])
def login():
  # Parse incoming JSON data
  data = request.get_json()
  print("Login request:" + str(data))
  # Check if full_name and work_email are provided
  if not data or "full_name" not in data or "work_email" not in data:
    return jsonify({"error": "Missing full_name or work_email"}), 400

  # Extract full_name and work_email from the request
  full_name = data["full_name"]
  work_email = data["work_email"]

  # Return the details as a response
  return jsonify({
    "message": "Login details received",
    "full_name": full_name,
    "work_email": work_email
  }), 200

# if __name__ == "__main__":
#     app.run(debug=True, port=8080, use_reloader=False)

@app.route("/conversation/<key>", methods=["GET"])
def get_conversation(key):
  """
    Retrieve the value for a specific key from conversation_store.
    """
  value = conversation_store.get(key)
  if value is None:
    return jsonify({"error": f"Key '{key}' not found"}), 404

  # Escape HTML in value for safety
  escaped_value = html.escape(value[0]['content'])
  return json.dumps({
    "value": escaped_value,
    "key": key}), 200


@app.route("/conversation/<key>", methods=["POST", "PUT"])
def upsert_conversation(key):
  """
    Upsert (insert/update) the value for a specific key in conversation_store.
    """
  data = request.get_json()
  if not data or "value" not in data:
    return jsonify({"error": "Missing 'value' in request data"}), 400

  value = html.unescape(data["value"])
  if key not in conversation_store:
    conversation_store[key] = [None]  # Initialize the list for the key if not exists

  conversation_store[key][0]['content'] = value

  return jsonify({"message": f"Key '{key}' has been set", "key": key, "value": value}), 200
