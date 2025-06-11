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
    print("Chat request:" + data)

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