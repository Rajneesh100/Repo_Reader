import requests
import os
from dotenv import load_dotenv


load_dotenv(dotenv_path="../.env")

API_KEY = os.getenv('API_KEY')
ENDPOINT = os.getenv('ENDPOINT')

def llm_response(prompt):
    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY
    }
    payload = {
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 2000
    }
    try:
        response = requests.post(ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"Error making request: {str(e)}"
