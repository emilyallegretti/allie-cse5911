import pandas as pd
import pytest
from datetime import datetime
from States.State import State, subtract_millisecond
from States.WatchingVideo import WatchingVideo
from States.OnMicroblogPage import OnMicroblogPage
from States.OnVideoPage import OnVideoPage

@pytest.fixture
def test_events():
    return [
        {'user_id': '1', 'timestamp': '2023-03-03 00:00:00.000', 'kind': 'PageEntry', 'page': 'Home'},
        {'user_id': '1', 'timestamp': '2023-03-03 00:05:00.000', 'kind': 'Logout', 'page': 'Logout Page'},
    ]

# Test subtract_millisecond utility function
def test_subtract_millisecond():
    timestamp = '2023-03-20 10:00:00.123000'
    expected = '2023-03-20 10:00:00.122000'
    assert subtract_millisecond(timestamp) == expected

# Test State.populateOrderedEvents static method
def test_populateOrderedEvents(test_events):
    ordered_events = State.populateOrderedEvents(test_events)
    assert ordered_events == [
        {'user_id': '1', 'kind': 'PageEntry', 'timestamp': '2023-03-03 00:00:00.000', 'page': 'Home'},
        {'user_id': '1', 'kind': 'PageExit', 'timestamp': '2023-03-03 00:04:59.999000',  'page': 'Home'},
        {'user_id': '1', 'kind': 'Logout', 'timestamp': '2023-03-03 00:05:00.000',  'page': 'Logout Page'}
    ]

# Test WatchingVideo from States
def test_watching_video_state():
    user_id, video_id = "2", "video2"
    start_time = datetime.strptime("2024-03-03 00:00:00", "%Y-%m-%d %H:%M:%S")
    end_time = datetime.strptime("2024-03-03 01:00:00", "%Y-%m-%d %H:%M:%S")
    watching_video = WatchingVideo(user_id, video_id, start_time, end_time, kind="PlayVideo")
    assert watching_video.user_id == user_id
    assert watching_video.videoId == video_id
    assert watching_video.startTime == start_time
    assert watching_video.endTime == end_time
    assert watching_video.kind == "PlayVideo"

# Test OnMicroblogPage from States
def test_on_microblog_page_state():
    user_id = "2"
    start_time = datetime.strptime("2024-03-03 06:00:00", "%Y-%m-%d %H:%M:%S")
    end_time = datetime.strptime("2024-03-03 07:00:00", "%Y-%m-%d %H:%M:%S")
    on_microblog_page = OnMicroblogPage(user_id, start_time, end_time, kind="Microblog_details")
    assert on_microblog_page.user_id == user_id
    assert on_microblog_page.startTime == start_time
    assert on_microblog_page.endTime == end_time
    assert on_microblog_page.kind == "Microblog_details"

# Test OnVideoPage from States
def test_on_video_page_state():
    user_id = "2"
    start_time = datetime.strptime("2024-03-03 10:01:00", "%Y-%m-%d %H:%M:%S")
    end_time = datetime.strptime("2024-03-03 10:02:00", "%Y-%m-%d %H:%M:%S")
    on_video_page = OnVideoPage(user_id, start_time, end_time, kind="PageEntry")
    assert on_video_page.user_id == user_id
    assert on_video_page.startTime == start_time
    assert on_video_page.endTime == end_time
    assert on_video_page.kind == "PageEntry"
