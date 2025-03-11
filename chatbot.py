import requests
import time
import json

API_KEY = 'KEY'
with open('../api_key.env', 'r') as file:
    API_KEY = file.read().replace('\n', '')

LLM_URL = (
    f'https://generativelanguage.googleapis.com/v1beta/models/'
    f'gemini-2.0-flash:generateContent?key={API_KEY}'
)

def query_llm(prompt):
    time.sleep(4)
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{
            "parts": [{"text": prompt}],
        }]
    }
    try:
        response = requests.post(LLM_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        text = data.get('candidates', [])[0].get('content', {}).get('parts', [])[0].get('text', '')
        return text
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None

def ask_question(question):
    print(question)
    return input("Your answer: ")

if __name__ == "__main__":
    decision_tree_code = """
if user_responses['age'] == 'old':
    if user_responses['gender'] == 'male':
        profile = 'old male'
    else:
        profile = 'old female'
else:
    if user_responses['gender'] == 'male':
        profile = 'young male'
    else:
        profile = 'young female'
"""

    user_responses = {}
    decision_tree_context = f"Decision tree logic: {decision_tree_code}"
    initial_prompt = f"What is the first question to ask the user to start profiling? Provide the question and the corresponding field name from the decision tree, separated by a colon. Give just the question and field name without any redundant text or explanation.\n{decision_tree_context}"
    # print(f'Prompt: {initial_prompt}')
    next_question_response = query_llm(initial_prompt)
    profile_not_identified = True

    while profile_not_identified:
        next_question, field_name = next_question_response.split(':')
        answer = ask_question(next_question.strip())
        user_responses[field_name.strip()] = answer
        decision_tree_context = f"Current user responses: {json.dumps(user_responses)}\nDecision tree logic: {decision_tree_code}"
        next_prompt = f"Given the user's answers so far, and the decision tree logic, what is the next question to ask? Provide the question and the Y, separated by a colon. If no more questions are needed, respond with 'No more questions needed'. Give just the question and field name without any redundant text or explanation.\n{decision_tree_context}"
        
        next_question_response = query_llm(next_prompt)

        if next_question_response.lower().strip() == 'no more questions needed':
            profile_not_identified = False



    final_prompt = f"Based on the decision tree logic and the user's responses, which profile does the user belong to? Be concise and write only the profile without explanations.\n{decision_tree_context}"
    profile = query_llm(final_prompt)
    print(f"Identified Profile: {profile}")