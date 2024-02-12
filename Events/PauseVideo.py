from Events.Event import Event
# class representing a 'pause video' event, with associated video id.
class PauseVideo(Event):
    def __init__(self, metadata, videoId):
        super().__init__(metadata, self.__class__.__name__)
        self.videoId = videoId
