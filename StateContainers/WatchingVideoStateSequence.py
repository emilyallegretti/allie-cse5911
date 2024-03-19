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

#TODO: account for case where user plays a video and then moves to new page without pausing the video first, or else this method wont catch it
# or what if the video completes (the user has watched the whole thing)? Is that logged as a pause, will the database account for that?
    def _getStates(self, video_df: pd.DataFrame):
        # dataframe is already sorted on construction of event seq
        states = []
        starttime = None
        for row in video_df.values:
            print(row)
            # row[1] is type of event, row[2] is timestamp, row[3] is videoid
            print(row[1])
            if row[1]=='PlayVideo':
                starttime=row[2]
            if row[1]=='PauseVideo':
                endtime = row[2]
                states.append((WatchingVideo(row[0], self.video_id, starttime, endtime, 'WatchingVideo')).__dict__)
                print(states)
        return states


