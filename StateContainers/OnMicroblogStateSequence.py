# each OnMicroblogSequence represents a Dataframe containing all of a specific user's microblog page duration sessions.

import  pandas as pd
from States.OnMicroblogPage import OnMicroblogPage

from States.State import State


class OnMicroblogSequence():
    # events_df should be a dataframe that includes PageExit events
    def __init__(self, events_df, user_id):
        events_df = events_df[events_df['user_id']==user_id]
        self._states=self.getStates(events_df)
        # convert _states to a dataframe of state objects
        self.states_df = pd.DataFrame.from_dict(self._states)

    # creates a list of all OnMicroblogPage state objects associated with the specific userId
        # TODO: Microblog enter and exit events could be made into an EventSequence to make this method easier
    def getStates(self, events_df: pd.DataFrame):
        states = []
        # first make sure df is sorted by timestamp
        events_df.sort_values('timestamp')
        # algorithm: iterate through dataframe. whenever a 'page entry' event is found with page=Microblog_details,
        # store this timestamp, and then continue iterating until a 'page exit' event is found with page=Microblog_details.
        # Store that timestamp and create a State object for this duration of being on Microblog. Add it to self.states
        # as a dict object
        starttime = None
        for row in events_df.values:
            print('in microblog state sequence')
            print(row)
            # index 1 corresponds to 'kind' attribute, 3 to 'page', 2 to 'timestamp'
            if row[1] == 'PageEntry' and row[3] == 'Microblog_details':
                starttime = row[2]
            if row[1] =='PageExit' and row[3] == 'Microblog_details': 
                endtime = row[2]
                # create new State and append it to running list
                states.append(
                    (
                        OnMicroblogPage(
                            row[0],
                            starttime,
                            endtime,
                            "OnMicroblogPage"
                        )
                    ).__dict__
                )
        return(states)
