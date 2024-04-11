import pandas as pd
from Events.Event import Event
# this EventContainer takes a userId and a videoId as parameters in its constructor and creates a 
# Pandas dataframe representing the user's pause and play events for that specific videoId, sorted by timestamp.
class VideoWatchSequence:
    def __init__(self, userId, videoId ):
        self.videoEventsDf = pd.DataFrame()
        # first get a list of only pause/play video events
        videoEvents= VideoWatchSequence._filterEvents()
        # create dataframe out of resulting list
        df = pd.DataFrame.from_dict(videoEvents)
        # print(df)
        # print(videoId)
        # print(userId)
        if df.empty:
            return
        else:
            # create instance variable that filters this df based on userId, videoId
            filtered_videoEventsDf = df[(df['user_id'] == userId) & (df['videoId']==videoId)].sort_values("timestamp")
            if filtered_videoEventsDf.empty:
                return
            else:
                self.videoEventsDf = filtered_videoEventsDf
                print(self.videoEventsDf)
        # create instance variable that filters this df based on userId, videoId
        # self.videoEventsDf = df[(df['user_id'] == userId) & (df['videoId']==videoId)].sort_values("timestamp")
        # print(self.videoEventsDf)


    # filters Event.events to get only pause and play events
    @staticmethod
    def _filterEvents():
        list=[]
        for item in Event.events:
            className=item['kind']
            if className=='PlayVideo' or className=='PauseVideo':
                list.append(item)
        return list

