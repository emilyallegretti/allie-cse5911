from States.State import State
import pandas as pd


# each OnVideoPage represents a duration of time in which the associated user is on the videos page.
class OnVideoPage(State):
    def __init__(self, userId, startTime, endTime, kind):
        super().__init__(userId, startTime, endTime, kind)

