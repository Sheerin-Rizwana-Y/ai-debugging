from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from extensions import db
from models.chat import Chat
from llm.core import complete_code

bp = Blueprint("complete", __name__)

@bp.route("/complete", methods=["POST"])
@login_required
def complete():
    try:
        code = request.get_json().get("code", "").strip()
        if not code:
            return jsonify({"error": "No code provided"}), 400

        completed_code = complete_code(code)
        if not completed_code:
            logger.warning(f"LLM returned empty completion for user {current_user.id}")
            return jsonify({"error": "LLM failed to complete code"}), 500
        

        chat = Chat(user_id=current_user.id, message=code, response=completed_code)
        db.session.add(chat)
        db.session.commit()

        return jsonify({"completed_code": completed_code})
    except Exception as e:
        logger.exception(f"LLM completion error for user {current_user.id}: {e}")
        return jsonify({"error": "Unexpected server error"}), 500