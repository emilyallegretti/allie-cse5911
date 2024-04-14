from Events.Event import Event

# class for emoji select event
class EmojiSelect(Event):
    def __init__(self, metadata, emojiType):
        super().__init__(metadata, self.__class__.__name__)
        self.emojiType = emojiType
