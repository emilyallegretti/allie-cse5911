from Events.Event import Event

# Class representing any PageEntry event
class PageEntry(Event):
    def __init__(self, metadata):
        super().__init__(metadata, self.__class__.__name__)
