# every instance of this class represents an Announcement post.
class Announcement:
    # keep a list of all Announcement objects created, stored as dictionaries
    announcements = []
    def __init__(self, id, annHead, annBody, date, authorId):
        self.id=id
        self.annHead=annHead
        self.annBody=annBody
        self.date=date
        self.authorId=authorId
    
    @staticmethod
    # adds an Announcement to announcements list.
    def add(announcement):
        Announcement.announcements.append(announcement.__dict__)
    
