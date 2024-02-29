from States.State import State
import pandas as pd

# each OnMicroblogPage represents a duration of time in which the associated user is on a discussion board page (given microblog Id).
class OnMicroblogPage(State):
    def __init__(self, userId, microblogId, startTime, endTime):
        super().__init__(userId, startTime, endTime)
        self.microblogId=microblogId
        



