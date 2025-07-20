import os
import requests
import logging

# 🔧 Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔐 Load API config
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "meta-llama/llama-3-8b-instruct:nitro"

def query_llm(prompt: str, model: str = None, system_message: str = None) -> str:
    # 🔐 Validate API key
    if not OPENROUTER_API_KEY:
        logger.error("❌ Missing OPENROUTER_API_KEY in environment")
        return "LLM Error: Missing API key"

    # 🧠 Validate prompt
    if not prompt or not isinstance(prompt, str) or not prompt.strip():
        logger.error("🛑 Invalid or empty prompt sent to LLM")
        return "LLM Error: Invalid prompt"

    model = model or DEFAULT_MODEL

    # 💬 Construct messages
    messages = []
    if system_message:
        messages.append({"role": "system", "content": system_message})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": model,
        "messages": messages
    }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    # 🐞 Log request (can disable in prod)
    logger.info(f"📤 Sending prompt to OpenRouter:\n{prompt}")
    logger.debug(f"📦 Payload: {payload}")

    try:
        response = requests.post(
            OPENROUTER_URL,
            json=payload,
            headers=headers,
            timeout=15  # 🕒 Add timeout to prevent hanging
        )
        response.raise_for_status()
        result = response.json()

        # ✅ Extract response content
        message = result["choices"][0]["message"]["content"]

        # 📊 Optional: log usage info
        usage = result.get("usage")
        if usage:
            logger.info(f"🔄 OpenRouter usage: {usage}")

        return message

    except requests.exceptions.Timeout:
        logger.error("⏱️ Request to OpenRouter timed out")
        return "LLM Error: Request timed out"

    except requests.exceptions.ConnectionError:
        logger.error("🔌 Unable to reach OpenRouter server")
        return "LLM Error: Server unreachable"

    except requests.exceptions.HTTPError as http_err:
        logger.error(f"❌ HTTP {http_err.response.status_code}: {http_err.response.text}")
        return f"LLM Error: HTTP {http_err.response.status_code} — {http_err.response.text}"

    except Exception as e:
        logger.error(f"⚠️ Unexpected error when querying LLM: {str(e)}")
        return f"LLM Error: {str(e)}"
