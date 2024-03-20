 # each LoggedIn represents a duration of time in which the associated user is logged into the platform.
from States.State import State


class LoggedIn(State):
    def __init__(self, userId, startTime, endTime):
        super().__init__(userId, startTime, endTime, __class__.__name__)