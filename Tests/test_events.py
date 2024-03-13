import pytest
from Events.Event import Event
from Events.Login import Login
from Events.Logout import Logout
from Events.UserActivity import UserActivity, create_user_activity

# Test Event Addition
def test_event_addition():
    Event.events.clear()
    length = len(Event.events)
    event_list = [
        {'kind': 'Login', 'user_id': '2', 'timestamp': '2024-03-03 00:00:00'},
        {'kind': 'Logout', 'user_id': '2', 'timestamp': '2024-03-03 01:00:00'},
    ]
    event_kind_mapping = {
        'Login': Login,
        'Logout': Logout,
    }

    for index, metadata in enumerate(event_list, start=1):
        kind = event_kind_mapping.get(metadata['kind'])
        if not kind:
            raise ValueError(f"Unknown event kind: {metadata['kind']}")
        new_event = kind(metadata)
        
        Event.add(new_event)
        assert len(Event.events) == length + index, f"Expected count: {length + index}"
    
    # reset events to the initial state
    Event.events = Event.events[:len(Event.events)]

# Test User Activity Creation
@pytest.mark.parametrize("metadata, expected_activity_type", [
    ({'user_id': '1', 'timestamp': '2024-03-03 00:00:00', 'page': 'Login Page'}, 'Login Page'),
    ({'user_id': '2', 'timestamp': '2024-03-04 01:00:00', 'page': 'Home'}, 'Home'),
])

def test_user_activity_creation(metadata, expected_activity_type):
    user_activity = create_user_activity(metadata)
    assert isinstance(user_activity, UserActivity), "Expected to create a UserActivity instance."
    assert user_activity.activityType == expected_activity_type, f"Expected activityType to be {expected_activity_type}."
    assert user_activity.user_id == metadata['user_id'], "The user_id should match the input data."
    assert user_activity.timestamp == metadata['timestamp'], "The timestamp should match the input data."