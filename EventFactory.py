'''
Initialize Event objects
'''
from Events.Login import Login
from Events.Logout import Logout
from Events.MouseEnterSlides import MouseEnterSlides
from Events.MouseLeaveSlides import MouseLeaveSlides
from Events.PageEntry import PageEntry
from Events.PauseVideo import PauseVideo
from Events.PlayVideo import PlayVideo

def create_event_object(row):
    event_type = row['kind']
    metadata = {
        'id': row['id'],
        'timestamp': row['timestamp'],
        'username': row['username'],
        'userid': row['user_id'],
        'page': row['page'],
        'action': row['action']
    }
    
    if event_type == 'Login':
        return Login(metadata)
    elif event_type == 'Logout':
        return Logout(metadata)
    elif event_type == 'Reading slides':
        if row['action'] == 'mouseenter':
            return MouseEnterSlides(metadata)
        elif row['action'] == 'mouseleave':
            return MouseLeaveSlides(metadata)
        else:
            return PageEntry(metadata)
    elif event_type == 'Page Entry':
        # check if this is a video pause/play event
        if row['action'] == 'pause':
            return PauseVideo(metadata)
        elif row['action'] == 'play':
            return PlayVideo(metadata)
        # todo : more elifs for page entry objects for each type of page?
        else:
            return PageEntry(metadata)
    else:
        print("No events so far")
