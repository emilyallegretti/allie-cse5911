# each instance of this class represents a Comment on a specific Microblog.
class Comment:
    def __init__(self, commentId, comment, createdDate, updatedDate, authorId, microblogId):
        self.commentId=commentId
        self.comment=comment
        self.createdDate=createdDate
        self.updatedDate=updatedDate
        self.authorId=authorId
        self.microblogId=microblogId