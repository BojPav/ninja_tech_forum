from handlers.base import BaseHandler
from models.topic import Topic
from google.appengine.api import users, memcache
import uuid
from models.comment import Comment

class TopicCreateHandler(BaseHandler):
    def get(self):

        user = users.get_current_user() # get user info
        csrf_token = str(uuid.uuid4()) # convert UUID to a string
        memcache.add(key=csrf_token, value=user.email(), time=3600) # put token to memcache

        params = {"csrf_token": csrf_token} # sending token to html page

        return self.render_template("topic_create.html", params=params)

    def post(self):

        # check if user is logged in
        user = users.get_current_user()
        if not user:
            return self.write("Please Log In")

        # CSRF protection
        csrf_token = self.request.get("csrf_token") # get token from html
        csrf_value = memcache.get(key=csrf_token) # get token from memcache

        if csrf_value != user.email(): # comparing tokens
            return self.write("You are a goddam hacker...!!!")

        # Add new topic
        topic_title = self.request.get("title")
        the_content = self.request.get("content")

        # if user logged in - creating new topic and saves in Datastore
        new_topic = Topic(title=topic_title, content=the_content, author_email=user.email())
        new_topic.put()

        return self.redirect_to("topic-details", topic_id=new_topic.key.id())


class TopicDetailsHandler(BaseHandler):
    def get(self, topic_id):
        topic = Topic.get_by_id(int(topic_id)) # get topic
        comments = Comment.query(Comment.topic_id == topic.key.id(), Comment.deleted == False).order(Comment.created).fetch()

        csrf_token = str(uuid.uuid4())
        memcache.add(key=csrf_token, value=True, time=3600)

        params = {"topic": topic, "comments": comments, "csrf_token": csrf_token}

        return self.render_template("topic_details.html", params=params)
