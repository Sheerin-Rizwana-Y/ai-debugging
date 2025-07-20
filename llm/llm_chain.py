import json
from llm.llm_client import query_llm
from models.prompt_log_model import log_prompt_chain

def run_prompt_chain(code: str, ml_result: dict, user_id=None) -> dict:
    context = {
        "code": code,
        "language": ml_result.get("language", "Unknown"),
        "error_type": ml_result.get("error_type", "Unknown")
    }

    # 🧠 Step 1: Ask LLM to identify each error as a structured JSON object
    prompt_1 = (
        f"The following code is written in {context['language']}:\n\n{context['code']}\n\n"
        "Identify all errors. For each error, output a JSON object like:\n"
        '{"line": <number>, "type": "<ErrorType>", "message": "<explanation>"}\n'
        "Return a JSON array of such objects. Do not include any extra commentary."
    )
    diagnosis = query_llm(prompt_1)

    # 🛡️ Try to parse structured output — fallback to empty list if invalid
    try:
        parsed_diagnosis = json.loads(diagnosis)
        if not isinstance(parsed_diagnosis, list):
            raise ValueError("Diagnosis is not a JSON array")
    except Exception:
        parsed_diagnosis = []
        diagnosis = "❌ LLM failed to return valid JSON diagnosis."

    # 🛠️ Step 2: Request corrected code
    prompt_2 = (
        f"The following errors were found in the code:\n{parsed_diagnosis}\n\n"
        "Rewrite the complete corrected code, applying all fixes. Return the code inside triple backticks, with no other text."
    )
    fix = query_llm(prompt_2)
    if not fix or "LLM Error" in fix:
        fix = "❌ LLM failed to generate a corrected version."

    # 💬 Step 3: Request explanation of the fix
    prompt_3 = (
        f"{fix}\nExplain how these changes resolved the listed errors."
    )
    explanation = query_llm(prompt_3)
    if not explanation or "LLM Error" in explanation:
        explanation = "❌ LLM failed to explain the correction."

    # 📦 Combine results
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
