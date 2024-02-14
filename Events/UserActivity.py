from Events.Event import Event

class UserActivity(Event):
    def __init__(self, metadata, activityType, activityDetails=None):
        super().__init__(metadata, self.__class__.__name__)
        self.activityType = activityType


def create_user_activity(row):
    metadata = {
        'user_id': row['user_id'],
        'timestamp': row['date'],
        'user_name': row['value2']
    }
    return UserActivity(metadata, row['value1'], row)

