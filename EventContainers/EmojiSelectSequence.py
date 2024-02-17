import pandas as pd
from Events.Event import Event

# This EventContainer takes a userId and a emojiType as parameters in its constructor and creates a 
# pandas DataFrame representing the user's emoji selection events for that specific userId, sorted by timestamp 
# and including calculated intensity and emotion scores.

class EmojiSelectSequence:
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

    @classmethod
    def get_emoji_mapping(cls, emojiType):
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
        return cls.intensity_meanings.get(intensity), cls.emotion_meanings.get(emotion)

    def __init__(self, userId):
        emojiEvents = self._filterEvents()
        # print(emojiEvents)
        df = pd.DataFrame.from_dict(emojiEvents)
        self.emojiEventsDf = df[(df['user_id'] == userId) & (df['kind'] == 'EmojiSelect')].sort_values("timestamp")

        # scores are added into lists of intensity_scores and emotion_scores respectively
        self.emojiEventsDf['IntensityScore'], self.emojiEventsDf['EmotionScore'] = zip(*self.emojiEventsDf['emojiType'].apply(self.get_emoji_mapping))

    @staticmethod
    def _filterEvents():
        list = []
        for item in Event.events:
            if item['kind'] == 'EmojiSelect':
                list.append(item)
        return list


