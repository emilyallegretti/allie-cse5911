
from Events.Event import Event

# Class representing any PageEntry event
class PageEntry(Event):
    def __init__(self, metadata):
        super().__init__(metadata)

