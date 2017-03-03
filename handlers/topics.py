from handlers.base import BaseHandler
from models.topic import Topic
from google.appengine.api import users


class TopicCreateHandler(BaseHandler):
    def get(self):
        return self.render_template("topic_create.html")

    def post(self):
        topic_title = self.request.get("title")
        the_content = self.request.get("content")

        # checking if user is logged in
        user = users.get_current_user()
        if not user:
            return self.write("Please Log In")

        # if user logged in - creating new topic and saves in Datastore
        new_topic = Topic(title=topic_title, content=the_content, author_email=user.email())
        new_topic.put()

        return self.redirect_to("topic-details", topic_id=new_topic.key.id())


class TopicDetailsHandler(BaseHandler):
    def get(self, topic_id):
        topic = Topic.get_by_id(int(topic_id))
        params = {"topic": topic}

        return self.render_template("topic_details.html", params=params)
