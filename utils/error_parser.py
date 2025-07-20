import re

def extract_errors(code_output):
    """
    Extracts structured error messages from raw code output using regex.
    """
    error_pattern = re.compile(r"(File \".*?\", line \d+.*?)(?=\n\S|$)", re.DOTALL)
    matches = error_pattern.findall(code_output)
    return matches if matches else ["No errors found."]
