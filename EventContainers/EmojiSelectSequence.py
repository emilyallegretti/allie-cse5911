import pandas as pd
from Events.Event import Event

# This EventContainer takes a userId and a emojiType as parameters in its constructor and creates a 
# pandas DataFrame representing the user's emoji selection events for that specific userId, sorted by timestamp 
# and including calculated intensity and emotion scores.

class EmojiSelectSequence:
    # map intensity levels to numerical scores
    intensity_meanings = {
        'lowest': -2,
        'low': -1,
        'neutral': 0,
        'high': 1,
        'highest': 2
    }
    # map emotion extents to numerical scores
    emotion_meanings = {
        'most negative': -2,
        'negative': -1,
        'neutral': 0,
        'positive': 1,
        'most positive': 2
    }

    # determine the intensity and emotion scores for a emoji type/letter
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
    
    # initializes an EmojiSelectSequence instance for a given user by filtering and sorting their emoji selection events into a DataFrame, 
    # then calculating and appending intensity and emotion scores for each event
    def __init__(self, userId):
        emojiEvents = self._filterEvents()
        # print(emojiEvents)
        df = pd.DataFrame.from_dict(emojiEvents)
        self.emojiEventsDf = df[(df['user_id'] == userId) & (df['kind'] == 'EmojiSelect')].sort_values("timestamp")

        # scores are added into lists of intensity_scores and emotion_scores respectively
        self.emojiEventsDf['IntensityScore'], self.emojiEventsDf['EmotionScore'] = zip(*self.emojiEventsDf['emojiType'].apply(self.get_emoji_mapping))

    # filter and return a list of events of selecting emoji
    @staticmethod
    def _filterEvents():
        list = []
        for item in Event.events:
            if item['kind'] == 'EmojiSelect':
                list.append(item)
        return list
