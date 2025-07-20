from flask import Blueprint, render_template,redirect,url_for,flash
from flask_login import login_required, current_user
from extensions import db
from models.chat import Chat
from flask import flash

bp = Blueprint('chat', __name__)

@bp.route('/dashboard')
@login_required
def dashboard():
    history = Chat.query.filter_by(user_id=current_user.id).order_by(Chat.timestamp.desc()).all()
    return render_template('dashboard.html', history=history)

@bp.route('/clear_history', methods=['POST'])
@login_required
def clear_history():
    Chat.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    flash("Chat history cleared.", "success")
    return redirect(url_for('chat.dashboard'))


