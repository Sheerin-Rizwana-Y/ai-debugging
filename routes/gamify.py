from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from extensions import db
from models.score import Score

bp = Blueprint('gamify', __name__)

@bp.route('/gamify')
@login_required
def gamify():
    return render_template('gamify.html')

@bp.route('/submit_challenge', methods=['POST'])
@login_required
def submit_challenge():
    data = request.json
    score = Score(user_id=current_user.id, challenge_name=data['name'], score=data['score'])
    db.session.add(score)
    db.session.commit()
    return jsonify({'message': 'Score submitted!'})
