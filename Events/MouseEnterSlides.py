from Events.Event import Event
# This Event class represents the action in which a user's mouse cursor enters the slide deck shown on the Readings page.

class MouseEnterSlides(Event):
    def __init__(self, metadata, slideId):
        super().__init__(metadata, self.__class__.__name__)
        self.slideId = slideId
