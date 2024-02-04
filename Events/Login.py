from Events.Event import Event

# represents a Login event.
class Login(Event):
    def __init__(self, metadata):
        super().__init__(metadata)
