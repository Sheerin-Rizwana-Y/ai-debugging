from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from extensions import db
from models.chat import Chat
from llm.core import simulate_output

bp = Blueprint("simulate", __name__)

@bp.route("/simulate", methods=["POST"])
@login_required
def simulate():
    code = request.get_json().get("code", "")
    output = simulate_output(code)

    chat = Chat(user_id=current_user.id, message=code, response=output)
    db.session.add(chat)
    db.session.commit()

    return jsonify({"simulated_output": output})
