import pandas as pd
import pytest
from EventContainers.VideoWatchSequence import VideoWatchSequence
from Events.Event import Event
from StateContainers.OnMicroblogStateSequence import OnMicroblogSequence
from StateContainers.OnVideoPageStateSequence import OnVideoPageSequence
from StateContainers.WatchingVideoStateSequence import WatchingVideoStateSequence


@pytest.fixture(scope="module")
def setup_test_events():
    test_user_id = 1
    Event.events = [
        {
            "kind": "PlayVideo",
            "user_id": "2",
            "timestamp": "2024-03-03 00:00:00",
            "videoId": "video2",
        },
        {
            "kind": "PauseVideo",
            "user_id": "2",
            "timestamp": "2024-03-03 01:00:00",
            "videoId": "video2",
        },
        {
            "kind": "PlayVideo",
            "user_id": "2",
            "timestamp": "2024-03-03 03:00:00",
            "videoId": "video2",
        },
        {
            "kind": "PlayVideo",
            "user_id": "2",
            "timestamp": "2024-03-03 04:00:00",
            "videoId": "video2",
        },
        {
            "kind": "PauseVideo",
            "user_id": "2",
            "timestamp": "2024-03-03 05:00:00",
            "videoId": "video2",
        },
        {
            "kind": "PageEntry",
            "user_id": "2",
            "timestamp": "2024-03-03 06:00:00",
            "page": "Microblog_details",
        },
        {
            "kind": "PageExit",
            "user_id": "2",
            "timestamp": "2024-03-03 07:00:00",
            "page": "Microblog_details",
        },
        {
            "kind": "PageEntry",
            "user_id": "2",
            "timestamp": "2024-03-03 08:00:00",
            "page": "Microblog_details",
        },
        {
            "kind": "PageEntry",
            "user_id": "2",
            "timestamp": "2024-03-03 08:01:00",
            "page": "Microblog_details",
        },
        {
            "kind": "PageExit",
            "user_id": "2",
            "timestamp": "2024-03-03 09:00:00",
            "page": "Microblog_details",
        },
        {
            "kind": "PageEntry",
            "user_id": "2",
            "timestamp": "2024-03-03 10:01:00",
            "page": "Video",
        },
        {
            "kind": "PageExit",
            "user_id": "2",
            "timestamp": "2024-03-03 10:02:00",
            "page": "Video",
        },
        {
            "kind": "PageEntry",
            "user_id": "2",
            "timestamp": "2024-03-03 11:01:00",
            "page": "Video",
        },
        {
            "kind": "PageEntry",
            "user_id": "2",
            "timestamp": "2024-03-03 11:02:00",
            "page": "Video",
        },
        {
            "kind": "PageExit",
            "user_id": "2",
            "timestamp": "2024-03-03 12:02:00",
            "page": "Video",
        },
    ]
    original_events = Event.events.copy()
    yield test_user_id
    # reset Event.events to original state
    Event.events = original_events


# # Test correct creation of a WatchingVideoStateSequence from list of test events
# def test_watching_video_state(setup_test_events):
#     test_user_id = setup_test_events
#     sequence = WatchingVideoStateSequence(2, "video2")
#     assert sequence.states_df is not None
#     assert (
#         len(sequence.states_df) == 2
#     )  # number of video watching states should be 2


# # Test correct creation of an OnMicroblogStateSequence with correct number of states
# def test_on_microblog_state(setup_test_events):
#     test_user_id = setup_test_events
#     sequence = OnMicroblogSequence(test_user_id, pd.DataFrame.from_dict(Event.events))
#     assert sequence.states_df is not None
#     assert len(sequence.states_df) == 2  # 2 states should be created


# # Test correct creation of an OnVideoPageStateSequence with correct number of states
# def test_on_video_page_state(setup_test_events):
#     test_user_id = setup_test_events
#     sequence = OnVideoPageSequence(test_user_id, pd.DataFrame.from_dict(Event.events))
#     assert sequence.states_df is not None
#     assert len(sequence.states_df) == 2  # 2 states should be created
