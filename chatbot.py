from clarifier import DecisionTreeSession
from profiler import GeminiProfiler
from question_solver import solve_question

class Chatbot(object):
    def __init__(self, language, doc):
        self.__language = language
        self.__doc = doc
        self.__user_question = None
        self.__profiler = GeminiProfiler(language)
        self.__clarifier = None

    def get_response(self, user_message):
        if self.__clarifier is None:
            self.__user_question = user_message
            mermaid_graph = self.__profiler.ask_llm(self.__user_question, self.__doc)
            self.__clarifier = DecisionTreeSession(mermaid_graph, self.__language)

        current_question, summary = self.__clarifier.get_next_question(user_message)
        if summary is None:
            return current_question, None
        else:
            return None, solve_question(self.__user_question, summary, self.__doc, self.__language)