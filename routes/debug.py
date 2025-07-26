import re
import json
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from extensions import db
from models.chat import Chat
from ml_model.detect import predict_language_and_error
from llm.llm_chain import run_prompt_chain
from models.feedback import Feedback

bp = Blueprint("debug", __name__)

def extract_error_line(text: str) -> int | None:
    """
    Extract first error line number from LLM diagnosis text.
    Accepts formats like 'Line 2:', 'on line 3', 'at line 4', 'line: 5', etc.
    """
    matches = re.findall(r"(?:[Ll]ine[:\s]*|on line\s*|at line\s*)(\d+)", text)
    return int(matches[0]) if matches else None

@bp.route("/feedback", methods=["POST"])
@login_required
def feedback():
    data = request.get_json()
    chat_id = data.get("chat_id")
    rating = data.get("rating")
    comment = data.get("comment", "")

    if not chat_id or not rating:
        return jsonify({"error": "chat_id and rating required"}), 400

    feedback = Feedback(
        user_id=current_user.id,
        chat_id=chat_id,
        rating=rating,
        comment=comment
    )
    db.session.add(feedback)
    db.session.commit()
    return jsonify({"success": True})
@bp.route("/debug", methods=["POST"])
@login_required
def debug():
    # 1. Get code from frontend
    code = request.get_json().get("code", "").strip()
    if not code:
        return jsonify({"error": "No code provided"}), 400

    # 2. Run ML for language + error_type
    prediction = predict_language_and_error(code)
    language = prediction.get("language", "Unknown")
    error_type = prediction.get("error_type", "Unknown")
    if ("error" in error_type.lower() or "exception" in error_type.lower() or "randomforestclassifier" in error_type.lower()):
        error_type = "Unknown"

    # 3. Run LLM chain
    chained_response = run_prompt_chain(code, prediction, user_id=current_user.id)
    if not chained_response or "diagnosis" not in chained_response:
        return jsonify({"error": "LLM chaining failed"}), 500

    diagnosis = chained_response["diagnosis"]
    fix = chained_response["fix"]
    explanation = chained_response["explanation"]

    # 4. Try to parse all errors from LLM diagnosis (if JSON)
    error_lines = []
    try:
        parsed = json.loads(diagnosis)
        if isinstance(parsed, list):
            for err in parsed:
                # Defensive: ensure keys exist
                error_lines.append({
                    "line": err.get("line"),
                    "type": err.get("type", "Unknown"),
                    "message": err.get("message", "")
                })
        else:
            # fallback: treat as single error object
            error_lines.append({
                "line": parsed.get("line"),
                "type": parsed.get("type", "Unknown"),
                "message": parsed.get("message", "")
            })
    except Exception:
        # fallback: extract first error line as before
        error_line = extract_error_line(diagnosis)
        if error_line is not None:
            # Try to extract error type from diagnosis text after the line number
            match_type = re.search(rf"[Ll]ine[:\s]*{error_line}[:\s-]*([^\n:]+)", diagnosis)
            extracted_type = match_type.group(1).strip() if match_type else error_type
            error_lines.append({
                "line": error_line,
                "type": extracted_type if extracted_type else error_type,
                "message": "Detected via LLM"
            })

    # 5. Extract corrected code from markdown block
    combined_text = f"{diagnosis}\n{fix}\n{explanation}"
    match = re.search(r'```(?:python)?\n([\s\S]+?)```', combined_text)
    fixed_code = match.group(1).strip() if match else ""

    # 6. Clean explanation
    explanation_clean = combined_text.replace(match.group(0), '').strip() if match else combined_text.strip()

    # 7. Log chat
    chat = Chat(
        user_id=current_user.id,
        message=code,
        response=combined_text
    )
    db.session.add(chat)
    db.session.commit()

    # 8. Return response
    return jsonify({
            "language": language,
            "error_type": error_type,
            "explanation": explanation_clean,
            "fixed_code": fixed_code,
            "error_lines": error_lines
    })