from Events.Event import Event

# This Event class describes the action in which a user's mouse cursor leaves the slide deck on the Readings page.
class MouseLeaveSlides(Event):
    def __init__(self, metadata, slideId):
        super().__init__(metadata, self.__class__.__name__)
        self.slideId = slideId
