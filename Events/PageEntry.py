
from Events.Event import Event

# Class representing any PageEntry event, EXCEPT PageEntries that are on the Videos page.
class PageEntry(Event):
    def __init__(self, metadata):
        super().__init__(metadata)

