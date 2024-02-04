from Events.Event import Event
# represents a Logout event.
class Logout(Event):
    def __init__(self, metadata):
        super().__init__(metadata)