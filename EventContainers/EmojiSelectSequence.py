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
        self.emojiEventsDf = pd.DataFrame()
        emojiEvents = self._filterEvents()
        df = pd.DataFrame.from_dict(emojiEvents)
        if df.empty:
            return
        else:
            filtered_emojiEventsDf = df[(df['user_id'] == userId) & (df['kind'] == 'EmojiSelect')].sort_values("timestamp")
            if filtered_emojiEventsDf.empty:
                print(f"Because of no emoji events found for userId: {userId}, an empty DataFrame is created")
            else:
                # scores are added into lists of intensity_scores and emotion_scores respectively
                self.emojiEventsDf = filtered_emojiEventsDf
                self.emojiEventsDf['IntensityScore'], self.emojiEventsDf['EmotionScore'] = zip(*self.emojiEventsDf['emojiType'].apply(self.get_emoji_mapping))

    # filter and return a list of events of selecting emoji
    @staticmethod
    def _filterEvents():
        list = []
        for item in Event.events:
            if item['kind'] == 'EmojiSelect':
                list.append(item)
        return list

# EmojiIndicators class describes the student engagement for emoji activities 
# by measuring indicators like frequency, regularity, emometer, mindfulness, and their variables.
class EmojiIndicators:
    def __init__(self, emoji_events_df):
        # initialize the EmojiIndicators instance with emoji event data
        self.emoji_events_df = emoji_events_df

    def get_frequency(self):
        # Variable: Count of Selected Emojis
        return self.emoji_events_df.groupby('user_id').size()

    def get_regularity(self):
        # Variables: Time Intervals Between Emoji Selections, Standard Deviation of Time Intervals
        # A lower standard deviation suggests selecting emojis at more consistent intervals
        self.emoji_events_df['timestamp'] = pd.to_datetime(self.emoji_events_df['timestamp'])
        intervals = self.emoji_events_df.groupby('user_id')['timestamp'].apply(lambda x: x.sort_values().diff().dt.total_seconds())
        return intervals.groupby('user_id').std()

    def get_emometer_scores(self):
        # Variables: Intensity Scores, Emotion Scores, Baseline Scores, Average Scores, Variability
        # Standard deviation shows how much the user's intensity scores vary. A larger standard deviation means a greater range of intensity in the user's emoji selections.
        metrics = self.emoji_events_df.groupby('user_id').agg({
            'IntensityScore': ['first', 'mean', 'std'],
            'EmotionScore': ['first', 'mean', 'std']
        })
        metrics.columns = ['IntensityBaseline', 'IntensityAverage', 'IntensityStdDev',
                           'EmotionBaseline', 'EmotionAverage', 'EmotionStdDeviation']
        return metrics

    def get_mindfulness(self):
        # Variables: Diversity of Emoji Types Used, Changes in Emoji Use Over Time
        diversity = self.emoji_events_df.groupby('user_id')['emojiType'].nunique()
        return diversity
