# every instance of this class represents an Announcement post.
class Announcement:
    def __init__(self, id, annHead, annBody, date, authorId):
        self.id=id
        self.annHead=annHead
        self.annBody=annBody
        self.date=date
        self.authorId=authorId
