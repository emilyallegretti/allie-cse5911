from Events.Event import Event

class UserActivity(Event):
    def __init__(self, metadata, activityType, activityDetails=None):
        super().__init__(metadata, self.__class__.__name__)
        self.activityType = activityType


def create_user_activity(row):
    metadata = {
        'user_id': row['user_id'],
        'timestamp': row['timestamp'],
    }
    return UserActivity(metadata, row['page'], row)

