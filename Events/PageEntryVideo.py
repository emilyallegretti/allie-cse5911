from Events.Event import Event
# class representing specifically the Page Entry events with 'page' attribute of Video. This 
# is because there could be videoIds associated with these types of page entries.
class PageEntryVideo(Event):
    def __init__(self, metadata, videoId):
        super().__init__(metadata)
        self.videoId = videoId