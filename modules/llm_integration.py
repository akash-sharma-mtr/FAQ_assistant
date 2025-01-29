import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def get_llm_response(prompt):
    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo",
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {e}"
    

