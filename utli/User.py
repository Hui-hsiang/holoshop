from enum import Enum
class states(Enum):
    START = 0
    NEW_NAME = 1
    NEW_CASE = 2
    NEW_STEP = 3
    NEW_REACT = 4
    NEW_RESULT = 5
    INPUT_TIME = 6
    INPUT_SUBJECT = 7
    INPUT_CONTENT = 8
    INPUT_TODO = 9
    INPUT_OWNER = 10
    INPUT_DEADLINE = 11 
class groups(Enum):
    START = 0
    MEETING = 1
    ISSUE = 2
    CASE = 3
    INFO = 4
class User():
    def __init__(self, id):
        self.user_id = id
        self.state = states.START.value
        self.group = groups.START.value