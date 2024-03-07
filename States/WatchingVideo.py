from States.State import State
import pandas as pd


# each WatchingVideo represents a duration of time in which the associated user is watching a specific video.
class WatchingVideo(State):
    def __init__(self, userId, videoId, startTime, endTime, kind):
        super().__init__(userId, startTime, endTime, kind)
        self.videoId = videoId

