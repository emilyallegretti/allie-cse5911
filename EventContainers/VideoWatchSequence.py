import pandas as pd
from Events.Event import Event

from Events.PauseVideo import PauseVideo
from Events.PlayVideo import PlayVideo
# this EventContainer takes a userId and a videoId as parameters in its constructor and creates a 
# Pandas dataframe representing the user's pause and play events for that specific videoId, sorted by timestamp.
class VideoWatchSequence:
    def __init__(self, userId, videoId ):
        # first get a list of only pause/play video events
        videoEvents= VideoWatchSequence._filterEvents()
        print(videoEvents)
        # create dataframe out of resulting list
        df = pd.DataFrame.from_dict(videoEvents)
        # create instance variable that filters this df based on userId, videoId
        self.videoEventsDf = df[(df['user_id'] == userId) & (df['videoId']==videoId)].sort_values("timestamp")


    # filters Event.events to get only pause and play events
    @staticmethod
    def _filterEvents():
        list=[]
        for item in Event.events:
            className=item['kind']
            if className=='PlayVideo' or className=='PauseVideo':
                list.append(item)
        return list
