from flask import Flask
from dotenv import load_dotenv
import os
from flask import redirect, url_for
from flask_login import current_user
from models import prompt_log_model

load_dotenv()
app = Flask(__name__)
app.config.from_object('config.Config')

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('chat.dashboard'))
    return redirect(url_for('auth.login'))


from extensions import db, login_manager
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

def status():
    return {"status": "running", "llm": "enabled", "ml_model": "loaded"}

with app.app_context():
    from models import user, chat, score
    from routes import auth, chat as chat_bp, debug, gamify, analytics, nlp,complete,explain,simulate,run

    app.register_blueprint(auth.bp)
    app.register_blueprint(chat_bp.bp)
    app.register_blueprint(debug.bp)
    app.register_blueprint(gamify.bp)
    app.register_blueprint(analytics.bp)
    app.register_blueprint(nlp.bp)
    app.register_blueprint(complete.bp)
    app.register_blueprint(explain.bp)
    app.register_blueprint(simulate.bp)
    app.register_blueprint(run.bp)


    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
