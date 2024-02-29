# parent State class that describes an acitivty that exists for a period of time. a State is associated with a specific user, and 
# has a start time and end time. 
class State:
    def __init__(self, user_id, startTime, endTime):
        self.user_id = user_id
        self.startTime = startTime
        self.endTime = endTime
