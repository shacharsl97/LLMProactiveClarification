class Chatbot(object):
    def __init__(self):
        self.__profiler = None
        self.__clarifier = None
        self.__question_solver = None

    def get_response(self, user_message):
        # Put here the logic of whether to call the profiler, clarifier or question solver.
        pass