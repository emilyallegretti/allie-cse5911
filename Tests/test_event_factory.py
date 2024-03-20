import pytest
from EventFactory import create_event_object, create_announcement, create_comment, create_microblog
from Events.Login import Login
from Events.Logout import Logout
from Events.MouseEnterSlides import MouseEnterSlides
from Events.MouseLeaveSlides import MouseLeaveSlides
from Events.PageEntry import PageEntry
from Events.PauseVideo import PauseVideo
from Events.PlayVideo import PlayVideo
from Events.EmojiSelect import EmojiSelect
from Posts.Announcement import Announcement
from Posts.Comment import Comment
from Posts.Microblog import Microblog

# Test event object creation
@pytest.mark.parametrize("event_row_data, expected_type", [
    ({'kind': 'Login', 'user_id': 1, 'timestamp': '2024-03-01 00:00:00'}, Login),
    ({'kind': 'Logout', 'user_id': 1, 'timestamp': '2024-03-01 01:00:00'}, Logout),
    ({'kind': 'Reading slides', 'user_id': 1, 'timestamp': '2024-03-02', 'action': 'mouseenter', 'slide_id': 'slide1'}, MouseEnterSlides),
    ({'kind': 'Reading slides', 'user_id': 1, 'timestamp': '2024-03-02', 'action': 'mouseleave', 'slide_id': 'slide1'}, MouseLeaveSlides),
    ({'kind': 'Page Entry', 'user_id': 1, 'timestamp': '2024-03-03', 'action': 'pause', 'video_id': 'video1'}, PauseVideo),
    ({'kind': 'Page Entry', 'user_id': 1, 'timestamp': '2024-03-03', 'action': 'play', 'video_id': 'video1'}, PlayVideo),
    ({'kind': 'emoji_select', 'user_id': 1, 'timestamp': '2024-03-02', 'emoji_type': 'A'}, EmojiSelect),
    ({'kind': 'Page Entry', 'user_id': 1, 'timestamp': '2024-03-04', 'action': 'No action','page':'Microblog_details'}, PageEntry),
])

def test_create_event_object(event_row_data, expected_type):
    event = create_event_object(event_row_data)
    assert isinstance(event, expected_type), f"Expected {expected_type.__name__} to be created"
    assert event.user_id == event_row_data['user_id'], "User ID should match input event data"
    assert event.timestamp == event_row_data['timestamp'], "Timestamp should match input event data"

def test_create_event_with_invalid_kind():
    invalid_event_data = {'kind': 'NonExistentType', 'user_id': 1, 'timestamp': '2024-03-01 02:00:00'}
    event = create_event_object(invalid_event_data)
    assert event is None, "Expected no event to be created with an invalid event kind"

# Test post object creation
@pytest.mark.parametrize("create_function, post_row_data, expected_type", [
    (create_announcement, {'id': 1, 'ann_head': 'Test Announcement', 'ann_body': 'This is a announcement.', 'date': '2024-03-01', 'author_id': 1}, Announcement),
    (create_comment, {'comment_id': 1, 'comment': 'This is a comment.', 'created_date': '2024-03-01', 'updated_date': '2024-03-02', 'author_id': 1, 'microblog_id': 1}, Comment),
    (create_microblog, {'microblog_id': 1, 'title': 'Test Microblog', 'body': 'This is a microblog.', 'slug': 'test-microblog', 'created_date': '2024-03-01', 'updated_date': '2024-03-02', 'author_id': 1}, Microblog),
])
def test_create_post_object(create_function, post_row_data, expected_type):
    post = create_function(post_row_data)
    assert isinstance(post, expected_type), f"Expected object of type {expected_type.__name__} to be created"

def test_create_post_with_empty_ann_head():
    post_data = {'id': 1, 'ann_head': '', 'ann_body': 'This is a announcement.', 'date': '2024-03-01', 'author_id': 1}
    post = create_announcement(post_data)
    assert isinstance(post, Announcement), "An Announcement object should be created even with empty 'ann_head'"
    assert post.id == post_data['id'] and post.annHead == post_data['ann_head'] and post.annBody == post_data['ann_body'], "Announcement attributes should match the provided data"

