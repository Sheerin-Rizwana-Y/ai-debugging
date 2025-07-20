from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from extensions import db
from models.chat import Chat
from llm.core import explain_code

bp = Blueprint("explain", __name__)

@bp.route("/explain", methods=["POST"])
@login_required
def explain():
    code = request.get_json().get("code", "")
    explanation = explain_code(code)

    chat = Chat(user_id=current_user.id, message=code, response=explanation)
    db.session.add(chat)
    db.session.commit()

    return jsonify({"explanation": explanation})
