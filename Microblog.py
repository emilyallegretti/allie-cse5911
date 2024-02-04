# each instance of this class represents a Microblog post, each of which has associated Comments
class Microblog: 
    def __init__(self, microblogId, title, body, slug, createdDate, updatedDate, authorId):
        self.microblogId = microblogId
        self.title = title
        self.body=body
        self.slug=slug
        self.createdDate=createdDate
        self.updatedDate=updatedDate
        self.authorId=authorId

