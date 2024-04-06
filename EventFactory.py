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
from Events.EmojiSelect import EmojiSelect
from Posts.Announcement import Announcement
from Posts.Comment import Comment
from Posts.Microblog import Microblog


def create_event_object(row):
    event_type = row['kind']
    metadata = {
        'user_id': row['user_id'],
        'timestamp': row['timestamp'],
    }

    if event_type == 'Login':
        return Login(metadata)
    elif event_type == 'Logout':
        return Logout(metadata)
    elif event_type == 'Reading slides':
        if row['action'] == 'mouseenter':
            return MouseEnterSlides(metadata, row["slide_id"])
        elif row['action'] == 'mouseleave':
            return MouseLeaveSlides(metadata, row["slide_id"])
        else:
            return PageEntry(metadata)
    elif event_type == 'Page Entry':
        # check if this is a video pause/play event
        if row['action'] == 'pause':
            return PauseVideo(metadata, row['video_id'])
        elif row['action'] == 'play':
            return PlayVideo(metadata, row['video_id'])
        else:
            return PageEntry(metadata,row['page'])
    elif event_type == 'emoji_select':
        return EmojiSelect(metadata, row['emoji_type'])
    
# create an Announcement object 
def create_announcement(row):
    return Announcement(row['id'], row['ann_head'], row['ann_body'], row['date'], row['author_id'])

# create a Comment object
def create_comment(row):
    return Comment(row['comment_id'], row['comment'], row['created_date'], row['updated_date'], row['author_id'], row['microblog_id'])

# create a Microblog object
def create_microblog(row):
    return Microblog(row['microblog_id'], row['title'], row['body'], row['slug'], row['created_date'], row['updated_date'], row['author_id'])



