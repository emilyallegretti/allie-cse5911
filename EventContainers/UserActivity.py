from Events.Event import Event

class UserActivity():
    
    def __init__(self, metadata, activityType, page, activityDetails=None):
        self.metadata=metadata
        self.activityType = activityType
        self.page=page


def create_user_activity(self, row):
    metadata = {
        'user_id': row['user_id'],
        'timestamp': row['timestamp'],
    }
    return UserActivity(metadata, row['kind'], row['page'],row)

