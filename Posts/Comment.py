# each instance of this class represents a Comment on a specific Microblog.
class Comment:
    comments=[]
    def __init__(self, commentId, comment, createdDate, updatedDate, authorId, microblogId):
        self.commentId=commentId
        self.comment=comment
        self.createdDate=createdDate
        self.updatedDate=updatedDate
        self.authorId=authorId
        self.microblogId=microblogId
    
    @staticmethod
    # adds a Comment to comments list.
    def add(comment):
        Comment.comments.append(comment.__dict__)
    
    # cls is used here to access the class variable 'comments' that holds all comment instances
    @classmethod
    # returns all comments for a specific microblog
    def get_comments_for_microblog(cls, microblogId):
        comments = []
        for comment in cls.comments:
            if comment['microblogId'] == microblogId:
                comments.append(comment)
        return comments
    
    @classmethod
    # returns all comments by a specific author
    def get_comments_by_author(cls, author_id): 
        author_comments = []
        for comment in cls.comments:
            if comment['authorId'] == author_id:
                author_comments.append(comment)
        return author_comments
