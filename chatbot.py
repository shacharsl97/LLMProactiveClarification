import requests
import time
import json
from google import genai

API_KEY = 'KEY'
with open('../api_key.env', 'r') as file:
    API_KEY = file.read().replace('\n', '')

LLM_URL = (
    f'https://generativelanguage.googleapis.com/v1beta/models/'
    f'gemini-2.0-flash:generateContent?key={API_KEY}'
)

def query_llm(prompt):
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
    
def query_llm_structured(prompt):
    client = genai.Client(
        api_key=API_KEY,
    )

    model = "gemini-2.0-flash"
    contents = [
        genai.types.Content(
            role="user",
            parts=[
                genai.types.Part.from_text(text=prompt),
            ],
        ),
    ]
    generate_content_config = genai.types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
        response_mime_type="application/json",
        response_schema=genai.types.Schema(
            type = genai.types.Type.OBJECT,
            required = ["a.reasoning", "d.more_questions_needed"],
            properties = {
                "a.reasoning": genai.types.Schema(
                    type = genai.types.Type.STRING,
                ),
                "b.question": genai.types.Schema(
                    type = genai.types.Type.STRING,
                ),
                "c.field_name": genai.types.Schema(
                    type = genai.types.Type.STRING,
                ),
                "d.more_questions_needed": genai.types.Schema(
                    type = genai.types.Type.BOOLEAN,
                ),
            },
        ),
    )

    full_output = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        full_output += chunk.text
    return json.loads(full_output)

def ask_question(question):
    print(question)
    return input("Your answer: ")

if __name__ == "__main__":
    with open('decision_tree.txt', 'r') as file:
        decision_tree_code = file.read()

    structured_llm_prompt_format = """
    question to be asked based on the first conditional statement to be checked in order to determine the output of the decision tree logic?
    If instead, there is already enough information based on the user responses so far, set more_questions_needed to False,
    otherwise set it to True.
    """

    user_responses = {}
    decision_tree_context = f"Decision tree logic in python: {decision_tree_code}"
    initial_prompt = f"What is the first {structured_llm_prompt_format}\n{decision_tree_context}"
    # Provide your reasoning first, then the question as a natural human sentence, followed by another dollar sign and then the corresponding field name from the decision tree. Format: reasoning$question$field_name. So you must have exactly 2 dollar signs in your output.
    next_question_response = query_llm_structured(initial_prompt)
    print(f"initial_prompt: {initial_prompt}, \nnext_question_response: {next_question_response}")

    while next_question_response["d.more_questions_needed"]:
        next_question = next_question_response["b.question"]
        field_name = next_question_response["c.field_name"]
        answer = ask_question(next_question.strip())
        user_responses[field_name.strip()] = answer
        decision_tree_context = f"Decision tree logic in python: {decision_tree_code}\nUser responses so far: {json.dumps(user_responses)}"
        next_prompt = f"Given the user's answers so far, what is the next {structured_llm_prompt_format}\n{decision_tree_context}"
        
        next_question_response = query_llm_structured(next_prompt)

        print(f"Next prompt: {next_prompt}, \nnext_question_response: {next_question_response}")

    final_prompt = f"Based on the decision tree logic and the user's responses, summarize the user responses to a short description. Be concise.\n{decision_tree_context}\nUser responses: {json.dumps(user_responses)}"
    profile = query_llm(final_prompt)
    print(f"Identified Profile: {profile}")