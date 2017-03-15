from google.appengine.ext import ndb
# from google.appengine.api import taskqueue


class Subscriber(ndb.Model):
    subscribe_email = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    deleted = ndb.BooleanProperty(default=False)

    @classmethod
    def create(cls, subscribe_email):
        subscriber = Subscriber(subscribe_email=subscribe_email)
        subscriber.put()

        #  background task for sending e-mail
        #taskqueue.add(url="/task/email-new-comment", params={"topic_author_email": topic.author_email,
        #                                                    "topic_title": topic.title,
        #                                                    "comment_content": comment.content})

        return subscriber