import os
import requests
import logging
import traceback
import json
from dotenv import load_dotenv


# 🔧 Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔐 Load API config
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "qwen/qwen3-coder:free"  # Fallback to widely supported default

def query_llm(prompt: str, model: str = None, system_message: str = None) -> str:
    load_dotenv()
    api_key=os.getenv("OPENROUTER_API_KEY")
    api_key=api_key.strip()
    # 🔐 API Key check
    if not api_key:
        logger.error("❌ OPENROUTER_API_KEY not set")
        return "LLM Error: Missing API key"

    # 🧠 Prompt check
    if not prompt or not isinstance(prompt, str) or not prompt.strip():
        logger.error("🛑 Empty or invalid prompt")
        return "LLM Error: Invalid prompt"

    model = model or DEFAULT_MODEL
    logger.info(f"🔍 Using model: {model}")
    logger.info(f"API KEY STARTS WITH: {OPENROUTER_API_KEY[:6]}")

    # 💬 Build messages
    messages = []
    if system_message:
        messages.append({"role": "system", "content": system_message})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": model,
        "messages": messages
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    logger.info("📤 Sending prompt to OpenRouter")
    logger.debug(f"📦 Payload: {json.dumps(payload, indent=2)}")

    try:
        response = requests.post(
            OPENROUTER_URL,
            json=payload,
            headers=headers,
            timeout=15  # Timeout for reliability
        )

        logger.info(f"🔎 Status code: {response.status_code}: {response.reason}")
        logger.debug(f"🔎 Raw response: {response.text[:400]}")

        result=response.json()

        if "error" in result:
            logger.error(f"❌ OpenRouter error: {result['error']}")
            return f"LLM Error: {result['error'].get('message', 'Server returned error')}"
        
        
        content = result.get("choices", [{}])[0].get("message", {}).get("content")
        if not content:
            logger.error("❌ Missing content in response")
            return "LLM Error: No response content found"

        return content

    except requests.exceptions.Timeout:
        logger.error("⏱️ Timeout reached while connecting to LLM server")
        return "LLM Error: Request timed out"

    except requests.exceptions.ConnectionError:
        logger.error("🔌 Could not establish connection with LLM server")
        return "LLM Error: Server unreachable"

    except requests.exceptions.HTTPError as http_err:
        logger.error(f"❌ HTTP Error: {http_err}")
        return "LLM Error: HTTP failure"

    except Exception as e:
        logger.error("⚠️ Unexpected exception during LLM request")
        logger.error(traceback.format_exc())
        return "LLM Error: Internal client failure"