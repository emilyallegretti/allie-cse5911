'''
Initialize Event objects
'''
from Events.Login import Login
from Events.Logout import Logout

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
    else:
        print("No events so far")
