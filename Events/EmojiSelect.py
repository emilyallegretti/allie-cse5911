from Events.Event import Event
class EmojiSelect(Event):
    def __init__(self, metadata, emojiType):
        super().__init__(metadata, self.__class__.__name__)
        self.emojiType = emojiType
    
    intensity_meanings = {
        'lowest': -2,
        'low': -1,
        'neutral': 0,
        'high': 1,
        'highest': 2
    }
   
    emotion_meanings = {
        'most negative': -2,
        'negative': -1,
        'neutral': 0,
        'positive': 1,
        'most positive': 2
    }
    
    @staticmethod
    def get_emoji_mapping(emojiType):
        emoji_mapping = {
            'A': ('highest', 'most negative'),
            'B': ('highest', 'negative'),
            'C': ('highest', 'neutral'),
            'D': ('highest', 'positive'),
            'E': ('highest', 'most positive'),
            'F': ('high', 'most negative'),
            'G': ('high', 'most positive'),
            'H': ('lowest', 'most negative'),
            'I': ('neutral', 'neutral'),
            'J': ('neutral', 'most positive'),
            'K': ('low', 'most negative'),
            'L': ('low', 'most positive'),
            'M': ('lowest', 'most negative'),
            'N': ('lowest', 'negative'),
            'O': ('lowest', 'neutral'),
            'P': ('lowest', 'positive'),
            'Q': ('lowest', 'most positive')
        }
        intensity, emotion = emoji_mapping.get(emojiType, ('none', 'none'))
        return EmojiSelect.intensity_meanings.get(intensity), EmojiSelect.emotion_meanings.get(emotion)
    