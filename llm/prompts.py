def get_debug_prompt(code, errors):
    error_summary = "\n".join([
        f"Line {e['line']}: {e['type']} — {e['message']}" for e in errors
    ])

    return f"""
You're a code debugging assistant for multiple languages.

Here's a code snippet:

{code}

Detected issues:
{error_summary}

Please:
1. Explain the errors.
2. Return a corrected version of the code.

Format your response as:

Explanation:
...

Fixed Code:
```<language>
...corrected code here..."""


def get_explanation_prompt(code):
    return f"""Explain what the following code does, step by step:

{code}"""

def get_completion_prompt(code):
    return f"""The following code is incomplete. Complete it logically:

{code}"""

def get_conversion_prompt(code, target_language):
    return f"""Convert the following code to {target_language}:

{code}"""

def get_nlp_prompt(query):
    return f"""You are a helpful assistant. Respond to this query in a clear and concise way:

{query}"""

def get_simulation_prompt(code):
    return f"""Given the following code, simulate its output as if it were executed. Show only the final printed result.\n\n{code}"""
