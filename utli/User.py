from enum import Enum
class states(Enum):
    START = 0
    GETORDER = 1
class groups(Enum):
    START = 0

class User():
    def __init__(self, id):
        self.user_id = id
        self.state = states.START.value
