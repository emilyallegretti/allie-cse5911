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
