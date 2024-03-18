import pytest
from Events.Event import Event
from EventContainers.EmojiSelectSequence import EmojiSelectSequence

@pytest.fixture(scope="module")
def setup_emoji_events():
    test_user_id = 1
    Event.events = [
        {'user_id': test_user_id, 'timestamp': '2024-03-01 00:00:00', 'kind': 'EmojiSelect', 'emojiType': 'A'},
        {'user_id': test_user_id, 'timestamp': '2024-03-01 00:05:00', 'kind': 'EmojiSelect', 'emojiType': 'B'},
        {'user_id': test_user_id, 'timestamp': '2024-03-01 00:08:00', 'kind': 'EmojiSelect', 'emojiType': 'C'},
    ]
    original_events = Event.events.copy()
    yield test_user_id
    # reset Event.events to original state
    Event.events = original_events

def test_emoji_select_sequence_init(setup_emoji_events):
    test_user_id = setup_emoji_events
    sequence = EmojiSelectSequence(test_user_id)
    assert sequence.emojiEventsDf is not None
    assert len(sequence.emojiEventsDf) == len(Event.events)

def test_emoji_event_sorting(setup_emoji_events):
    test_user_id = setup_emoji_events
    sequence = EmojiSelectSequence(test_user_id)
    timestamps = sequence.emojiEventsDf['timestamp'].tolist()
    # check if DataFrame is sorted
    assert timestamps == sorted(timestamps)

def test_intensity_emotion_score_mapping(setup_emoji_events):
    test_user_id = setup_emoji_events
    sequence = EmojiSelectSequence(test_user_id)
    # check if intensity and emotion scores are matched
    for _, row in sequence.emojiEventsDf.iterrows():
        intensity, emotion = EmojiSelectSequence.get_emoji_mapping(row['emojiType'])
        assert row['IntensityScore'] == intensity
        assert row['EmotionScore'] == emotion
