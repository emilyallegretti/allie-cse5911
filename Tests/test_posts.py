import pytest
from Posts.Announcement import Announcement
from Posts.Comment import Comment
from Posts.Microblog import Microblog

# Test Post Addition
def test_announcement_addition():
    announcement = Announcement(id=1, annHead="Test Announcement", annBody="This is an announcement.", date="2024-03-01", authorId=1)
    Announcement.add(announcement)
    found = any(ann for ann in Announcement.announcements if ann['id'] == announcement.id and 
                ann['annHead'] == announcement.annHead and ann['annBody'] == announcement.annBody and 
                ann['date'] == announcement.date and ann['authorId'] == announcement.authorId)
    
    assert found, "Announcement should be added to the list"
    Announcement.announcements.clear()

def test_microblog_addition():
    microblog = Microblog(microblogId=1, title="Test Microblog", body="This is a microblog.", slug="test-microblog", createdDate="2024-03-01", updatedDate="2024-03-02", authorId=1)
    Microblog.add(microblog)
    found = any(mb for mb in Microblog.microblogs if mb['microblogId'] == microblog.microblogId and 
                mb['title'] == microblog.title and mb['body'] == microblog.body and 
                mb['slug'] == microblog.slug and mb['createdDate'] == microblog.createdDate and 
                mb['updatedDate'] == microblog.updatedDate and mb['authorId'] == microblog.authorId
            ) 
    
    assert found, "Microblog should be added to the list"
    Microblog.microblogs.clear()

def test_comment_addition():
    comment = Comment(commentId=1, comment="Test comment", createdDate="2024-03-01", updatedDate="2024-03-02", authorId=1, microblogId=1)
    Comment.add(comment)
    assert any(com['commentId'] == comment.commentId for com in Comment.comments), "Comment should be added to the list"


# Test Comments Retrieval
def test_get_comments_for_microblog():
    Comment.comments.clear()
    comments = [
        Comment(commentId=1, comment="Comment on microblog 1", createdDate="2024-03-01", updatedDate="2024-03-02", authorId=1, microblogId=1),
        Comment(commentId=2, comment="Comment on microblog 2", createdDate="2024-03-03", updatedDate="2024-03-04", authorId=2, microblogId=2),
    ]
    for comment in comments:
        Comment.add(comment)

    comments_for_microblog1 = Comment.get_comments_for_microblog(1)
    assert len(comments_for_microblog1) == 1 and all(com['microblogId'] == 1 for com in comments_for_microblog1), "Should retrieve comments for microblog 1 only"

def test_get_comments_by_author():
    Comment.comments.clear()
    comments = [
        Comment(commentId=1, comment="Author 1's comment", createdDate="2024-03-01", updatedDate="2024-03-02", authorId=1, microblogId=1),
        Comment(commentId=2, comment="Author 2's comment", createdDate="2024-03-02", updatedDate="2024-03-04", authorId=2, microblogId=2),
    ]
    for comment in comments:
        Comment.add(comment)

    comments_by_author1 = Comment.get_comments_by_author(1)
    assert len(comments_by_author1) == 1 and all(com['authorId'] == 1 for com in comments_by_author1), "Should retrieve comments by author 1 only"

def test_count_comments_by_author():
    Comment.comments.clear()
    comments = [
        Comment(commentId=1, comment="Author 1's comment", createdDate="2024-03-01", updatedDate="2024-03-02", authorId=1, microblogId=1),
        Comment(commentId=2, comment="Author 1's second comment", createdDate="2024-03-02", updatedDate="2024-03-04", authorId=1, microblogId=2),
    ]
    for comment in comments:
        Comment.add(comment)

    count_comments_by_author1 = Comment.count_comments_by_author(1)
    assert count_comments_by_author1 == 2, "Should count comments by author 1"

def test_average_comment_length_by_author():
    Comment.comments.clear()
    comments = [
        Comment(commentId=1, comment="Author 1's comment", createdDate="2024-03-01", updatedDate="2024-03-02", authorId=1, microblogId=1),
        Comment(commentId=2, comment="Author 1's second comment", createdDate="2024-03-02", updatedDate="2024-03-04", authorId=1, microblogId=2),
    ]
    for comment in comments:
        Comment.add(comment)

    average_comment_length_by_author1 = Comment.average_comment_length_by_author(1)
    assert average_comment_length_by_author1 == 21.5, "Should calculate average comment length by author 1"
