from flask import Flask
from dotenv import load_dotenv
import os
from flask import redirect, url_for
from flask_login import current_user
from models import prompt_log_model
import httpx
from extensions import db,login_manager

load_dotenv()
app = Flask(__name__)
app.config.from_object('config.Config')
app.secret_key=os.getenv("SECRET_KEY","fallback-secret")

# Flask-Login setup
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('chat.dashboard'))
    return redirect(url_for('auth.login'))

@app.route("/test-llm")
def test_llm():
    from llm.llm_client import query_llm
    try:
        result = query_llm("Say hello")
        return result
    except Exception as e:
        print("LLM Error:", traceback.format_exc())
        return "LLM call failed"

@app.before_request
def check_system():
    if not os.getenv("OPENROUTER_API_KEY"):
        return "⚠️ Missing OpenRouter API key", 503

def status():
    return "Server is alive"

with app.app_context():
    from models import user, chat, score
    from routes import auth, chat as chat_bp, debug, gamify, analytics
    from routes import nlp,complete,explain,simulate,run

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
    app.run(debug=True,host='0.0.0.0')
