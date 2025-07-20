from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from extensions import db
from models.chat import Chat
from llm.core import complete_code

bp = Blueprint("complete", __name__)

@bp.route("/complete", methods=["POST"])
@login_required
def complete():
    code = request.get_json().get("code", "")
    completed_code = complete_code(code)

    chat = Chat(user_id=current_user.id, message=code, response=completed_code)
    db.session.add(chat)
    db.session.commit()

    return jsonify({"completed_code": completed_code})
