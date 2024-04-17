import pandas as pd
from Events.Event import Event
class UserActivity(Event):

    # Initializes the UserActivity object with metadata, activity type, and page details.
    def __init__(self, metadata, activityType, page, activityDetails=None):
        super().__init__(metadata, self.__class__.__name__)
        self.activityType = activityType
        self.page = page

    # Static method to create a UserActivity instance from a DataFrame row.
    @staticmethod
    def create_user_activity(row):
        metadata = {
            'user_id': row['user_id'],
            'timestamp': row['timestamp'],
        }
        return UserActivity(metadata, row['kind'], row['page'], row)

# Function to calculate total time spent per day for a user or all users.
def calculate_time_spent_per_day(activities, user_id=None):
    # Convert activities to a DataFrame if not already one.
    if not isinstance(activities, pd.DataFrame):
        df_activities = pd.DataFrame([vars(a) for a in activities])
    else:
        df_activities = activities

    # Convert timestamps to datetime objects and extract date.
    df_activities['timestamp'] = pd.to_datetime(df_activities['timestamp'])
    df_activities['date'] = df_activities['timestamp'].dt.date

    # Filter activities by user ID if provided.
    if user_id is not None:
        df_activities = df_activities[df_activities['user_id'] == user_id].copy()

    df_activities = df_activities.sort_values(by=['user_id', 'timestamp'])

    # Calculate the first and last activity times per day for each user.
    time_spent = df_activities.groupby(['user_id', 'date']).agg(
        first_activity=('timestamp', 'min'),
        last_activity=('timestamp', 'max')
    )
    
    # Compute the total time spent in seconds and format it.
    time_spent['total_time_spent_seconds'] = (time_spent['last_activity'] - time_spent['first_activity']).dt.total_seconds()
    time_spent['total_time_spent'] = time_spent['total_time_spent_seconds'].apply(
        lambda x: f"{int(x // 3600)}h {int((x % 3600) // 60)}m")

    return time_spent[['total_time_spent']].reset_index()

# Function to count login activities per day.
def count_login_page_activities_per_day(activities, user_id=None):
    # Convert list to DataFrame if not already one.
    if not isinstance(activities, pd.DataFrame):
        df_activities = pd.DataFrame([vars(a) for a in activities])
    else:
        df_activities = activities

    # Parse timestamps to date.
    df_activities['timestamp'] = pd.to_datetime(df_activities['timestamp'])
    df_activities['date'] = df_activities['timestamp'].dt.date
    
    # Filter for 'Login' activity type.
    login_activities = df_activities[df_activities['activityType'] == 'Login']
    
    # Filter by user ID if provided.
    if user_id is not None:
        login_activities = login_activities[login_activities['user_id'] == user_id]

    # Count logins per day.
    login_count_per_user_day = login_activities.groupby(['user_id', 'date']).size().reset_index(name='login_count')
    
    return login_count_per_user_day

# Function to count daily visits to the 'Modules' page for a specified user.
def count_readings_page_visits_for_user(activities, user_id):
    # Convert list to DataFrame if needed.
    if not isinstance(activities, pd.DataFrame):
        df_activities = pd.DataFrame([vars(a) for a in activities])
    else:
        df_activities = activities

    # Convert timestamps to date.
    df_activities['timestamp'] = pd.to_datetime(df_activities['timestamp'])
    df_activities['date'] = df_activities['timestamp'].dt.date
    
    # Filter for visits to 'Modules' by specific user.
    readings_activities = df_activities[(df_activities['user_id'] == user_id) & (df_activities['page'] == 'Modules')]

    # Count visits per day.
    readings_count_per_day = readings_activities.groupby('date').size().reset_index(name='readings_visit_count')
    
    return readings_count_per_day

# Function to calculate the time spent on 'Modules' page per day for a specified user.
def calculate_time_spent_on_readings_per_day(activities, user_id):
    # Convert list to DataFrame if not already one.
    if not isinstance(activities, pd.DataFrame):
        df_activities = pd.DataFrame([vars(a) for a in activities])
    else:
        df_activities = activities

    # Sort by timestamp after filtering for specific user.
    user_activities = df_activities[df_activities['user_id'] == user_id]
    user_activities = user_activities.sort_values('timestamp')
    
    # Convert timestamps to date.
    user_activities['timestamp'] = pd.to_datetime(user_activities['timestamp'])
    user_activities['date'] = user_activities['timestamp'].dt.date

    # Focus on 'Modules' page activities and calculate time between activities.
    readings_activities = user_activities[user_activities['page'] == 'Modules'].copy()
    readings_activities['next_timestamp'] = readings_activities['timestamp'].shift(-1)
    readings_activities['time_spent_seconds'] = (readings_activities['next_timestamp'] - readings_activities['timestamp']).dt.total_seconds()

    # Aggregate time spent per day.
    time_spent_per_day = readings_activities.groupby('date')['time_spent_seconds'].sum().reset_index()
    time_spent_per_day['time_spent'] = time_spent_per_day['time_spent_seconds'].apply(
        lambda x: f"{int(x // 3600)}h {int((x % 3600) // 60)}m {int(x % 60)}s")

    return time_spent_per_day[['date', 'time_spent']]
