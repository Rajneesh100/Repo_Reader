import requests


API_KEY = "e72d7df09d524b469c1fbfdf61a6cdd2"
ENDPOINT = "https://trabii-test-ai.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview"


def llm_response(prompt):
    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY
    }
    payload = {
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 2000
    }
    try:
        response = requests.post(ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"Error making request: {str(e)}"


# import requests
# import re
# import json

# API_KEY = "e72d7df09d524b469c1fbfdf61a6cdd2"
# ENDPOINT = "https://trabii-test-ai.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview"

# def llm_response(prompt):
#     headers = {
#         "Content-Type": "application/json",
#         "api-key": API_KEY
#     }
#     payload = {
#         "messages": [{"role": "user", "content": prompt}],
#         "temperature": 0.7,
#         "max_tokens": 2000
#     }
#     try:
#         response = requests.post(ENDPOINT, headers=headers, json=payload)
#         response.raise_for_status()
#         raw_text = response.json()["choices"][0]["message"]["content"]

#         # Extract any executable code (SQL, Bash, Python, etc.)
#         code_blocks = re.findall(r"```(.*?)```", raw_text, re.DOTALL)
#         code = "\n".join(code_blocks) if code_blocks else ""

#         # Construct the standardized JSON response
#         formatted_response = {
#             "Response": raw_text.strip(),
#             "have_executable_code": bool(code_blocks),
#             "code": code
#         }

#         return json.dumps(formatted_response, indent=4)

#     except requests.exceptions.RequestException as e:
#         return json.dumps({
#             "Response": f"Error making request: {str(e)}",
#             "have_executable_code": False,
#             "code": ""
#         }, indent=4)


