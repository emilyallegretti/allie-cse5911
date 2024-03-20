import pandas as pd
from Events.Event import Event
class UserActivity(Event):

    def __init__(self, metadata, activityType, page, activityDetails=None):
        super().__init__(metadata, self.__class__.__name__)
        self.activityType = activityType
        self.page=page

    @staticmethod
    def create_user_activity(row):
        metadata = {
            'user_id': row['user_id'],
            'timestamp': row['timestamp'],
        }
        return UserActivity(metadata, row['kind'], row['page'],row)


def calculate_time_spent_per_day(activities, user_id=None):
        if not isinstance(activities, pd.DataFrame):
            df_activities = pd.DataFrame([vars(a) for a in activities])
        else:
            df_activities = activities

        df_activities['timestamp'] = pd.to_datetime(df_activities['timestamp'])
        df_activities['date'] = df_activities['timestamp'].dt.date

        if user_id is not None:
            df_activities = df_activities[df_activities['user_id'] == user_id].copy()

        df_activities = df_activities.sort_values(by=['user_id', 'timestamp'])

        time_spent = df_activities.groupby(['user_id', 'date']).agg(
            first_activity=('timestamp', 'min'),
            last_activity=('timestamp', 'max')
        )
        
        time_spent['total_time_spent_seconds'] = (time_spent['last_activity'] - time_spent['first_activity']).dt.total_seconds()
        time_spent['total_time_spent'] = time_spent['total_time_spent_seconds'].apply(
            lambda x: f"{int(x // 3600)}h {int((x % 3600) // 60)}m")

        return time_spent[['total_time_spent']].reset_index()
        

def count_login_page_activities_per_day(activities, user_id=None):
        if not isinstance(activities, pd.DataFrame):
            df_activities = pd.DataFrame([vars(a) for a in activities])
        else:
            df_activities = activities

        df_activities['timestamp'] = pd.to_datetime(df_activities['timestamp'])
        df_activities['date'] = df_activities['timestamp'].dt.date
        
        login_activities = df_activities[df_activities['activityType'] == 'Login']
        
        if user_id is not None:
            login_activities = login_activities[login_activities['user_id'] == user_id]

        login_count_per_user_day = login_activities.groupby(['user_id', 'date']).size().reset_index(name='login_count')
        
        return login_count_per_user_day



