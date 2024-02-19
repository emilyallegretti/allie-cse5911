# each instance of this class represents a Microblog post, each of which has associated Comments
from Posts.Comment import Comment
class Microblog:
    microblogs=[]
    def __init__(self, microblogId, title, body, slug, createdDate, updatedDate, authorId):
        self.microblogId = microblogId
        self.title = title
        self.body=body
        self.slug=slug
        self.createdDate=createdDate
        self.updatedDate=updatedDate
        self.authorId=authorId
    
    @staticmethod
    # adds a Microblog to microblogs list.
    def add(microblog):
        Microblog.microblogs.append(microblog.__dict__)