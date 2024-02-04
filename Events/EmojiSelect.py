from Events.Event import Event


class EmojiSelect(Event):
    def __init__(self, metadata, emojiType):
        super().__init__(metadata)
        self.emojiType = emojiType