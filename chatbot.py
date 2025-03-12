from clarifier import DecisionTreeSession

class Chatbot(object):
    def __init__(self):
        self.__profiler = None
        self.__clarifier = None
        self.__question_solver = None

        self.__init_all = True

    def get_response(self, user_message):
        if self.__init_all:
            self.__init_all = False
            mermaid_graph = None
            self.__clarifier = DecisionTreeSession(mermaid_graph)

        current_question, summary = self.__clarifier.get_next_question(user_message)
        if summary is None:
            return current_question, None
        else:
            return None, self.__question_solver(summary)