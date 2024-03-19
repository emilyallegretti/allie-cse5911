import pytest
from EventContainers.VideoWatchSequence import VideoWatchSequence
from Events.Event import Event
from Events.Login import Login
from Events.Logout import Logout
from Events.PauseVideo import PauseVideo
from Events.PlayVideo import PlayVideo
from Events.UserActivity import UserActivity, create_user_activity
from StateContainers.WatchingVideoStateSequence import WatchingVideoStateSequence


@pytest.fixture(scope="module")
def setup_video_watch_events():
    test_user_id = 1
    Event.events = [
        {"kind": "PauseVideo", "user_id": "2", "timestamp": "2024-03-03 00:00:00"},
        {"kind": "PauseVideo", "user_id": "2", "timestamp": "2024-03-03 01:00:00"},
        {"kind": "PlayVideo", "user_id": "2", "timestamp": "2024-03-03 03:00:00"},
        {"kind": "PlayVideo", "user_id": "2", "timestamp": "2024-03-03 04:00:00"},
        {"kind": "PauseVideo", "user_id": "2", "timestamp": "2024-03-03 05:00:00"}
    ]
    original_events = Event.events.copy()
    yield test_user_id
    # reset Event.events to original state
    Event.events = original_events


# Test correct creation of a WatchingVideoStateSequence
def test_video_watch_sequence_init(setup_video_watch_events):
    test_user_id = setup_video_watch_events
    sequence = WatchingVideoStateSequence(test_user_id, "video2")
    assert sequence.states_df is not None
    assert len(sequence.videoEventsDf) == len(Event.events)


def test_video_event_sorting(setup_video_watch_events):
    test_user_id = setup_video_watch_events
    sequence = VideoWatchSequence(test_user_id)
    timestamps = sequence.videoEventsDf["timestamp"].tolist()
    # check if DataFrame is sorted
    assert timestamps == sorted(timestamps)
