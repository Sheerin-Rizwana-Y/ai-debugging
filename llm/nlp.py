from llm.prompts import get_nlp_prompt
from llm.core import call_llm

def handle_nlp_query(query):
    prompt = get_nlp_prompt(query)
    return call_llm(prompt)

def simulate_output(code):
    prompt = f"""Simulate the output of the following code as if it were executed in its language.
Only show the printed or returned result:\n\n{code}"""
    return call_llm(prompt)
