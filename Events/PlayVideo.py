from Events.Event import Event
# class representing a 'play video' event, with associated video id.
class PlayVideo(Event):
    def __init__(self, metadata, videoId):
        super().__init__(metadata, self.__class__.__name__)
        self.videoId = videoId
