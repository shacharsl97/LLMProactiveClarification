from abc import ABC, abstractmethod
from google import genai

format = """	
	You are given a text taken from a website and a user question about the text. There are multiple possible answers directed by the profile of the user. Your task is to analyze the text and to identify different potential profiles. Profiles can be described using a decision tree for each facet in the profile. This decision tree will be used to query the user until a profile is matched. Output the decision tree in a mermaid.js.
	Please only return the mermaid.js graph
Question:  {question}
Text:
{website}
"""


class Profiler(ABC):

	@abstractmethod
	def ask_llm(self, query, website_content) -> str:
		raise NotImplementedError


class GeminiProfiler(Profiler):

	def __init__(self):
		from clarifier import API_KEY as GEMINI_API_KEY
		self.client = genai.Client(api_key=GEMINI_API_KEY)

	def ask_llm(self, query, website_content) -> str:
		prompt = format.format(question=query, website=website_content)
		response = self.client.models.generate_content(
			model="gemini-2.0-flash",
			contents=prompt
		)
		return response.text


if __name__ == '__main__':
	client = GeminiProfiler()
	mermaid = open("mermaid.txt").read()
	question = "כמה ימי חופשה מגיעים לי לאחר לידה?"
	print(client.ask_llm(question, mermaid))