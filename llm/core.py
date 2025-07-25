import httpx
import os
from dotenv import load_dotenv
from llm.prompts import (
    get_debug_prompt,
    get_explanation_prompt,
    get_completion_prompt,
    get_conversion_prompt,
    get_simulation_prompt,
    get_nlp_prompt
)

DEFAULT_MODEL = "gpt-3.5-turbo"


def call_llm(prompt, model=DEFAULT_MODEL):
    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
    if not api_key:
        return "❌ Missing OpenRouter API key."
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "http://localhost:5000",
        "X-Title": "Debug Assistant"
    }

    body = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = httpx.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body, timeout=30)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"❌ LLM error: {str(e)}"

def debug_code(code,errors):
    prompt = get_debug_prompt(code, errors)
    return call_llm(prompt)

def explain_code(code):
    prompt = get_explanation_prompt(code)
    return call_llm(prompt)

def complete_code(code):
    prompt = get_completion_prompt(code)
    return call_llm(prompt)

def convert_code(code, target_language):
    prompt = get_conversion_prompt(code, target_language)
    return call_llm(prompt)

def extract_errors(code):
    # Dummy placeholder
    return [
        {"line": 3, "type": "NameError", "message": "Variable 'reslt' not defined"},
        {"line": 5, "type": "ZeroDivisionError", "message": "Division by zero"}
    ]

def simulate_output(code):
    prompt = get_simulation_prompt(code)
    return call_llm(prompt)
