from abc import ABC

# superclass for all Events.
# metadata should be a key-value dictionary object containing metadata attributes common to all events:
# metadata = {id , timestamp, username, userid, page, action}
# Event acts as an abstract class that shouldn't be instantiated directly
class Event(ABC):
    # keep a static list of all Event objects created, stored as a list of dictionaries
    events=[]
    # add page attribute
    def __init__(self, metadata,kind):
        self.user_id=metadata['user_id']
        self.kind=kind
        self.timestamp = metadata["timestamp"]

    @staticmethod
    def add(event):
        Event.events.append(event.__dict__)
