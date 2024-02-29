# each OnMicroblogSequence represents a Dataframe containing all of a specific user's microblog page duration sessions.

class OnMicroblogSequence():
    def __init__(self, user_activities_df):
        states=getStates(user_activities_df)
        

    # creates a list of all OnMicroblogPage objects associated with the specific userId and microblogId.
    def getStates(user_activities_df):
        # first sort by timestamp
        user_activities_df.sort_values('timestamp')
        # if page type is Microblog_details, the timestamp is startTime of new Microblog session
        onMicroblog = False
        for event in user_activities_df:
            if event['page']=='Microblog_details':
                onMicroblog=True
            if 


        # if this is the last entry in the dataframe, don't count it (for now) TODO
