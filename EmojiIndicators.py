import pandas as pd
import numpy as np

class EmojiActivityTracker:
    def __init__(self, emoji_events_df):
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
