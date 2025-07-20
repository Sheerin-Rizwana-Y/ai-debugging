import os
import joblib

current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, "random_forest_model.pkl")

try:
    model = joblib.load(model_path)
    print("✅ Model loaded from:", model_path)
except Exception as e:
    raise RuntimeError(f"❌ Failed to load model: {e}")

def predict_language_and_error(code: str) -> dict:
    """
    Predicts language and error type using the unified model.
    Expected label format: 'Python_SyntaxError', 'C_MemoryError', etc.
    """
    feature_dict = extract_features(code)
    feature_vector = list(feature_dict.values())  # ✅ Convert to list of values

    try:
        raw_label = model.predict([feature_vector])[0]  # Output like 'Python_SyntaxError'
        language, error_type = raw_label.split("_", maxsplit=1)
    except Exception as e:
        language = "Unknown"
        error_type = f"Prediction error: {str(e)}"

    return {
        "language": language,
        "error_type": error_type
    }

def extract_features(code: str) -> dict:
    """
    Converts raw code string into a structured feature dict.
    These features should match what your model was trained on.
    """
    return {
        "length": len(code),
        "num_lines": code.count("\n"),
        "num_semicolons": code.count(";"),
        "has_print": int(any(kw in code for kw in ["print", "System.out.println", "cout"])),
        "has_loop": int(any(kw in code for kw in ["for", "while"])),
        "has_main": int("main" in code),
        "has_def": int("def" in code),
        "has_public": int("public" in code),
        "has_class": int(any(kw in code for kw in ["class", "struct"])),
        "has_function_kw": int(any(kw in code for kw in ["def", "func", "function"])),
        "has_error_kw": int(any(kw in code for kw in ["try", "catch", "except"])),
        "uses_curly_braces": int("{" in code or "}" in code)
    }
