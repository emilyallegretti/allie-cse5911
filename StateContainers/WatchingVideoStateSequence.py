# each WatchingVideoStateSequence represents a Dataframe containing all States in which a user is watching a specific video.
# Uses VideoWatchSequence EventContainer, which already contains a sequence of video pause/play events for a specific user/video.
import pandas as pd
from EventContainers.VideoWatchSequence import VideoWatchSequence
from States.State import State
from States.WatchingVideo import WatchingVideo


# creates a list of all WatchingVideo state objects associated with the specific userId
class WatchingVideoStateSequence:

    def __init__(self, user_id, video_id):
        self.user_id=user_id
        self.video_id=video_id
        # video_seq reps a dataframe of a user's pause and play events for video_id
        video_seq = VideoWatchSequence(user_id, video_id)
        self._states = self._getStates(video_seq.videoEventsDf)
        # convert _states to a dataframe of State objects
        self.states_df = pd.DataFrame.from_dict(self._states)

    # for Frequency indicator: counts the amount of video watching states there are in this states_df instance
    def countVideoFrequency(self):
        if self.states_df:
            return len(self.states_df)
        else:
            return 0
    # for video watching time indicator: accumulate total time spent watching this video by adding up time durations in this df
    #TODO: in future, this information could be used to track if the user has completed this video by comparing the total
    # watch time with the length of the video. However, at the current state of the database we do not know the length of the video. 
    def countTotalWatchTime(self):
        if self.states_df:
            df = self.states_df
             # Convert string timestamps to datetime objects
            df['startTime'] = pd.to_datetime(df['startTime'])
            df['endTime'] = pd.to_datetime(df['endTime'])
            
            # Calculate duration for each row
            df['duration'] = df['endTime'] - df['startTime']
            
            # Calculate total duration
            total_duration = df['duration'].sum()
            
            return total_duration


#TODO: account for case where user plays a video and then moves to new page without pausing the video first, or else this method wont catch it
# or what if the video completes (the user has watched the whole thing)? Is that logged as a pause, will the database account for that?
    def _getStates(self, video_df: pd.DataFrame):
        # dataframe is already sorted on construction of event seq
        states = []
        starttime = None
        for row in video_df.values:
            # row[1] is type of event, row[2] is timestamp, row[3] is videoid
            if row[1]=='PlayVideo':
                starttime=row[2]
            if row[1]=='PauseVideo' and starttime is not None:
                endtime = row[2]
                states.append((WatchingVideo(row[0], self.video_id, starttime, endtime, 'WatchingVideo')).__dict__)
                starttime = None
        return states


