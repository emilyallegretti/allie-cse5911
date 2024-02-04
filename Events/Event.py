from abc import ABC

# superclass for all Events.
# metadata should be a key-value dictionary object containing metadata attributes common to all events:
# metadata = {id , timestamp, username, userid, page, action}
# Event acts as an abstract class that shouldn't be instantiated directly
class Event(ABC):
    def __init__(self, metadata):
        self.id = id
        self.timestamp = metadata["timestamp"]
        self.username = metadata["username"]
        self.userid = metadata["userid"]
        self.page = metadata["page"]
        self.action = metadata['action']
