from Events.Event import Event


class MouseEnterSlides(Event):
    def __init__(self, metadata, slideId):
        super().__init__(metadata)
        self.slideId = slideId
