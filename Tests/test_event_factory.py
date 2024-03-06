import pytest
from EventFactory import create_event_object
from Events.Login import Login
from Events.Logout import Logout

def test_create_login_event():
    row = {'kind': 'Login', 'user_id': 1, 'timestamp': '2024-03-01 00:00:00'}
    event = create_event_object(row)
    assert isinstance(event, Login)
    assert event.user_id == row['user_id']

def test_create_logout_event():
    row = {'kind': 'Logout', 'user_id': 1, 'timestamp': '2024-03-01 01:00:00'}
    event = create_event_object(row)
    assert isinstance(event, Logout)
    assert event.user_id == row['user_id']

