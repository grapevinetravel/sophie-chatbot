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
    if not data or "message" not in data:
        return jsonify({"error": "Missing message"}), 400

    req = ChatRequest(**data)
    conv_id = req.conversation_id or str(uuid4())
    reply = run_chat(req.message, conv_id, conversation_store)
    return jsonify({"reply": reply, "conversation_id": conv_id})

# if __name__ == "__main__":
#     app.run(debug=True, port=8080, use_reloader=False)