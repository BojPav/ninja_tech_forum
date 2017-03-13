from handlers.base import BaseHandler
from models.topic import Topic
from models.comment import Comment
from google.appengine.api import users
from utils.decorators import validate_csrf


class TopicCreateHandler(BaseHandler):
    def get(self):
        return self.render_template_with_csrf("topic_create.html")

    @validate_csrf
    def post(self):

        # check if user is logged in
        user = users.get_current_user()
        if not user:
            return self.write("Please login, not allowed for unregistered users to post a topic...!")

        # Add new topic
        topic_title = self.request.get("title")
        topic_content = self.request.get("content")

        # if user logged in - create new topic and save in Datastore
        new_topic = Topic(title=topic_title, content=topic_content, author_email=user.email())
        new_topic.put()

        return self.redirect_to("topic-details", topic_id=new_topic.key.id())


class TopicDetailsHandler(BaseHandler):
    def get(self, topic_id):
        topic = Topic.get_by_id(int(topic_id))  # get topic

        comments = Comment.query(Comment.topic_id == topic.key.id(), Comment.deleted == False).order(Comment.created).fetch()

        params = {"topic": topic, "comments": comments}

        return self.render_template_with_csrf("topic_details.html", params=params)


class TopicDeleteHandler(BaseHandler):
    @validate_csrf
    def post(self, topic_id):
        topic = Topic.get_by_id(int(topic_id))

        user = users.get_current_user()

        if topic.author_email == user.email() or users.is_current_user_admin():
            Topic.delete(topic=topic)

        return self.redirect_to("main-page")
