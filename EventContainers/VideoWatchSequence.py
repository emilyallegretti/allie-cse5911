import pandas as pd
from Events.Event import Event
# this EventContainer takes a userId and a videoId as parameters in its constructor and creates a 
# Pandas dataframe representing the user's pause and play events for that specific videoId, sorted by timestamp.
class VideoWatchSequence:
    def __init__(self, userId, videoId ):
        # first get a list of only pause/play video events
        videoEvents= VideoWatchSequence._filterEvents()
        # create dataframe out of resulting list
        df = pd.DataFrame.from_dict(videoEvents)
        print(df)
        print(videoId)
        print(userId)
        # create instance variable that filters this df based on userId, videoId
        self.videoEventsDf = df[(df['user_id'] == userId) & (df['videoId']==videoId)].sort_values("timestamp")
        print(self.videoEventsDf)


    # filters Event.events to get only pause and play events
    @staticmethod
    def _filterEvents():
        list=[]
        for item in Event.events:
            className=item['kind']
            if className=='PlayVideo' or className=='PauseVideo':
                list.append(item)
        return list
    
    # take the entire container/list of events created
    # start a new empty list
    # for each event x in original container
        # if the event is a page entry event, and we are already in page p 
             # create a brand new page exit event for page p,
            # append page exit event to empty list 
        # append event x to new empty list 

