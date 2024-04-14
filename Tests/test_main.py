import pytest
from Main import create_event_objects, create_post_objects, create_events_dataframe, create_page_exits_dataframe

# Test 
def test_create_event_objects_empty():
    assert create_event_objects([]) is None

def test_create_post_objects_empty():
    assert create_post_objects([], 'announcement') is None

def test_create_events_dataframe_empty():
    assert create_events_dataframe([], "test") is None

def test_create_page_exits_dataframe_empty():
    assert create_page_exits_dataframe([]) is None