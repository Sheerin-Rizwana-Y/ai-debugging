from extensions import db
from datetime import datetime

class PromptLog(db.Model):
    __tablename__ = 'prompt_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=True)
    input_code = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(50))
    error_type = db.Column(db.String(50))
    prompts = db.Column(db.JSON, nullable=False)        # list of prompts used in chain
    responses = db.Column(db.JSON, nullable=False)      # list of LLM responses
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<PromptLog {self.id} — {self.language} | {self.error_type}>"

# 🔁 Utility function to log prompt chains
def log_prompt_chain(user_id, context, prompts, responses):
    new_log = PromptLog(
        user_id=user_id,
        input_code=context.get("code", ""),
        language=context.get("language", "Unknown"),
        error_type=context.get("error_type", "Unknown"),
        prompts=prompts,
        responses=[
            responses.get("diagnosis", ""),
            responses.get("fix", ""),
            responses.get("explanation", "") 
        ]
    )
    db.session.add(new_log)
    db.session.commit()
