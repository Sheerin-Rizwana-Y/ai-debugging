from flask import Blueprint, request, jsonify
from flask_login import login_required
from llm.nlp import handle_nlp_query

bp = Blueprint('nlp', __name__)

@bp.route('/nlp', methods=['POST'])
@login_required
def nlp():
    query = request.json.get('query')
    response = handle_nlp_query(query)
    return jsonify({'response': response})
