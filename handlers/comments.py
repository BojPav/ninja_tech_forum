from handlers.base import BaseHandler
from google.appengine.api import memcache
from google.appengine.api import users
from models.comment import Comment
from models.topic import Topic


class CommentAdd(BaseHandler):
    def post(self, topic_id):

        # CSRF protection
        csrf_token = self.request.get("csrf_token") # get token
        mem_token = memcache.get(key=csrf_token) # # check csrf-token from memcache

        if not mem_token: # if token does not exist in memcache
            return self.write("Oooo, you are hacker...!")

        # check if user is logged
        user = users.get_current_user()

        if not user:
            return self.write("Please login ! You are not allowed to post...")

        text = self.request.get("comment-text")
        topic = Topic.get_by_id(int(topic_id))

        comment = Comment(content=text, author_email=user.email(), topic_id=topic.key.id(), topic_title=topic.title)
        comment.put()

        return self.redirect_to("topic-details", topic_id=topic.key.id())
