from google.appengine.ext import ndb
from google.appengine.api import taskqueue


class Comment(ndb.Model):
    content = ndb.TextProperty()
    author_email = ndb.StringProperty()
    topic_id = ndb.IntegerProperty()
    topic_title = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    deleted = ndb.BooleanProperty(default=False)

    @classmethod
    def create(cls, content, author, topic):
        comment = Comment(content=content, author_email=author, topic_id=topic.key.id(), topic_title=topic.title)
        comment.put()

        #  background task for sending e-mail
        taskqueue.add(url="/task/email-new-comment", params={"topic_author_email": topic.author_email,
                                                             "topic_title": topic.title,
                                                             "comment_content": comment.content})

        return comment

    @classmethod
    def delete(cls, comment):
        comment.deleted = True
        comment.put()

        return comment
