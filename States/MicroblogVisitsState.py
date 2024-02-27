from States.State import State
import pandas as pd

class MicroblogVisitsState(State):
    def __init__(self, user_id, df_activities):
        super().__init__(user_id)
        # filter out microblog page entry visits for a given user
        self.df_activities = df_activities[(df_activities['user_id'] == user_id) & 
                                           (df_activities['activityType'] == 'Microblog')].copy()
        # convert timestamp to datetime, and extract the date
        self.df_activities['timestamp'] = pd.to_datetime(self.df_activities['timestamp'])
        self.df_activities['date'] = self.df_activities['timestamp'].dt.date
    
    def get_visit_counts(self):
        # count visits
        visit_counts = self.df_activities.groupby('date').size().reset_index(name='visit_count')
        # sort by date
        visit_counts_sorted = visit_counts.sort_values(by='date')
        return visit_counts_sorted
