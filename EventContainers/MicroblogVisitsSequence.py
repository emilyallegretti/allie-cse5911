import pandas as pd

# This EventContainer tracks and analyzes microblog page visits for a given user. 
# It takes a userId and a data frame of user activities as parameters in its constructor.
# It filters for microblog visits and counts visits by date.

class MicroblogVisitsSequence:
    def __init__(self, user_id, df_activities):
        self.user_id = user_id
        # filter out microblog page entry visits for a given user
        self.df_activities = df_activities[(df_activities['user_id'] == user_id) & 
                                           (df_activities['page'] == 'Microblog')].copy()
        # convert timestamp to datetime, and extract the date
        self.df_activities['timestamp'] = pd.to_datetime(self.df_activities['timestamp'])
        self.df_activities['date'] = self.df_activities['timestamp'].dt.date
    
    def count_microblog_visits(self):
        # count visits
        microblog_visits = self.df_activities.groupby('date').size().reset_index(name='visit_count')
        # sort by date
        microblog_visits_sorted = microblog_visits.sort_values(by='date')
        return microblog_visits_sorted
