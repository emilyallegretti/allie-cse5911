from Events.Event import Event


class MouseLeaveSlides(Event):
    def __init__(self, metadata, slideId):
        super().__init__(metadata, self.__class__.__name__)
        self.slideId = slideId
