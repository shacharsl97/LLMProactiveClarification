import requests
import json
from google import genai

class DecisionTreeSession:
    def __init__(self, mermaid_graph):
        with open('../api_key.env', 'r') as file:
            api_key = file.read().replace('\n', '')
        self.api_key = api_key
        self.mermaid_graph = mermaid_graph
        self.user_responses = {}
        self.LLM_URL = (
            f'https://generativelanguage.googleapis.com/v1beta/models/'
            f'gemini-2.0-flash:generateContent?key={api_key}'
        )
        self.__first_question = True
        self.next_question_response = None

    def query_llm(self, prompt):
        headers = {'Content-Type': 'application/json'}
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        try:
            response = requests.post(self.LLM_URL, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            text = data.get('candidates', [])[0].get('content', {}).get('parts', [])[0].get('text', '')
            return text
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
        
    def query_llm_structured(self, prompt):
        text = self.query_llm(prompt)
        try:
            # Extract the JSON part from the text
            json_start = text.find('[') + 1
            json_end = text.rfind(']')
            json_text = text[json_start:json_end]
            return json.loads(json_text)
        except json.JSONDecodeError:
            print("Failed to parse JSON. Raw response:", text)
            return {"error": "JSON parsing failed", "raw_response": text}

    def get_initial_question(self):
        initial_prompt = f"""
        Determine the first question based on the mermaid graph.
        If there is already enough information, set more_questions_needed to False, otherwise set it to True.

        <output>
        [
        {{
            "a.reasoning": "Reasoning towards determining the question",
            "b.question": "The question to be asked",
            "c.field_name": "The field name",
            "d.more_questions_needed": True/False
        }}
        ]
        </output>

        DAG in mermaid format:
        {self.mermaid_graph}
        """
        self.next_question_response = self.query_llm_structured(initial_prompt)
        return self.next_question_response

    def process_answer(self, answer):
        if not self.next_question_response or "error" in self.next_question_response:
            return self.next_question_response or {"error": "No initial question found."}

        field_name = self.next_question_response["c.field_name"].strip()
        self.user_responses[field_name] = answer.strip()
        
        next_prompt = f"""
        Given the user's answers so far, determine the next question.
        If there is already enough information, set more_questions_needed to False.

        <output>
        [
        {{
            "a.reasoning": "Reasoning towards determining the question",
            "b.question": "The question to be asked",
            "c.field_name": "The field name",
            "d.more_questions_needed": True/False
        }}
        ]
        </output>

        DAG in mermaid format:
        {self.mermaid_graph}

        User responses so far:
        {json.dumps(self.user_responses)}
        """
        
        self.next_question_response = self.query_llm_structured(next_prompt)
        return self.next_question_response

    def get_final_summary(self):
        final_prompt = f"""
        Summarize the user responses to a short description.
        The summary must be in Hebrew.
        Don't mention the field names, only relate to the meaning of the user responses.

        User responses:
        {json.dumps(self.user_responses)}
        
        DAG in mermaid format, for reference:
        {self.mermaid_graph}
        """
        return self.query_llm(final_prompt)

    def get_next_question(self, last_answer):
        """
        Returns next_question, summary.
        next_question is None if no more questions are needed.
        summary is None if more questions are needed.
        """
        if self.__first_question == True:
            self.__first_question = False
            next_question = self.get_initial_question()
        else:
            next_question = session.process_answer(last_answer)
        if next_question["d.more_questions_needed"]:
            return next_question["b.question"], None
        else:
            summary = session.get_final_summary()
            return None, summary

if __name__ == "__main__":
    with open('mermaid.txt', 'r', encoding="utf-8") as file:
        mermaid_graph = file.read()

    session = DecisionTreeSession(mermaid_graph)
    next_question = session.get_initial_question()

    # if True:
    while next_question["d.more_questions_needed"]:
        print(next_question["b.question"])
        answer = input("Enter your answer: ")
        next_question = session.process_answer(answer)

    summary = session.get_final_summary()
    print(summary)