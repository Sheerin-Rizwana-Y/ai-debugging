import json
from llm.llm_client import query_llm
from models.prompt_log_model import log_prompt_chain
import logging
import traceback

logger=logging.getLogger(__name__)

def run_prompt_chain(code: str, ml_result: dict, user_id=None) -> dict:
    context = {
        "code": code,
        "language": ml_result.get("language", "Unknown"),
        "error_type": ml_result.get("error_type", "Unknown")
    }
    
    logger.info(f"Starting LLM prompt chain with context: {user_id}")
    logger.info(f"Context: {context}")

    # 🧠 Step 1: Ask LLM to identify each error as a structured JSON object
    prompt_1 = (
        f"The following code is written in {context['language']}:\n\n{context['code']}\n\n"
        "Identify all errors. For each error, output a JSON object like:\n"
        '{"line": <number>, "type": "<ErrorType>", "message": "<explanation>"}\n'
        "Return a JSON array of such objects. Do not include any extra commentary."
    )
    
    try:
        logger.info("📤 Sending diagnosis prompt to LLM")
        diagnosis = query_llm(prompt_1)
    except Exception as e:
        diagnosis = "❌ LLM Error: Diagnosis request failed"
        logger.error("🚨 Diagnosis prompt failed")
        logger.error(traceback.format_exc())

    # 🛡️ Try to parse structured output — fallback to empty list if invalid
    try:
        parsed_diagnosis = json.loads(diagnosis)
        if not isinstance(parsed_diagnosis, list):
            raise ValueError("Diagnosis is not a JSON array")
    except Exception:
        parsed_diagnosis = []
        diagnosis = "❌ LLM failed to return valid JSON diagnosis."
        logger.warning("⚠️ Diagnosis parsing failed")

    # 🛠️ Step 2: Fix Prompt
    errors_json=json.dumps(parsed_diagnosis, indent=2)
    prompt_2 = (
        f"The following errors were found in the code:\n{errors_json}\n\n"
        "Rewrite the complete corrected code, applying all fixes. Return the code inside triple backticks, with no other text."
    )
    try:
        logger.info("📤 Sending fix prompt to LLM")
        fix = query_llm(prompt_2)
    except Exception as e:
        fix = "❌ LLM Error: Code fix request failed"
        logger.error("🚨 Fix prompt failed")
        logger.error(traceback.format_exc())

    
    # 💬 Step 3: Request explanation of the fix
    prompt_3 = (
        f"{fix}\nExplain how these changes resolved the listed errors."
    )
    try:
        logger.info("📤 Sending explanation prompt to LLM")
        explanation = query_llm(prompt_3)
    except Exception as e:
        explanation = "❌ LLM Error: Explanation request failed"
        logger.error("🚨 Explanation prompt failed")
        logger.error(traceback.format_exc())

    # 📦 Final response structure
    response_chain = {
        "diagnosis": diagnosis,
        "diagnosis_json": parsed_diagnosis,
        "fix": fix,
        "explanation": explanation
    }

    # 🗂️ Optional logging for fine-tuning pipeline
    if user_id:
        try:
            log_prompt_chain(
                user_id=user_id,
                context=context,
                prompts=[prompt_1, prompt_2, prompt_3],
                responses=response_chain
            )
        except Exception as e:
            print(f"⚠️ Failed to log prompt chain: {e}")

    return response_chain
