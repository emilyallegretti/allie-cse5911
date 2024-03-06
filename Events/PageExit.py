from Events.Event import Event

# Class representing a 'synthetic' PageExit event (meaning Page Exits aren't explicitly logged to the database,
# but created by us based off db logs)
class PageExit(Event):
    def __init__(self, metadata, page):
        super().__init__(metadata, self.__class__.__name__)
        self.page = page
