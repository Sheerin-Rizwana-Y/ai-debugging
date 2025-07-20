from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.score import Score

bp = Blueprint('analytics', __name__)

@bp.route('/analytics')
@login_required
def analytics():
    scores = Score.query.filter_by(user_id=current_user.id).all()
    return render_template('analytics.html', scores=scores)
