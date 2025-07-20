import black

def format_code(code: str) -> str:
    """
    Formats Python code using Black.
    """
    try:
        formatted = black.format_str(code, mode=black.FileMode())
        return formatted
    except Exception as e:
        return f"Formatting failed: {str(e)}"
