from handlers.base import BaseHandler
from google.appengine.api import mail


class EmailNewCommentWorker(BaseHandler):
    def post(self):
        topic_author_email = self.request.get("topic_author_email")
        topic_title = self.request.get("topic_title")
        topic_id = self.request.get("topic_id")

        mail.send_mail(sender="pavlovicbojan86@gmail.com",
                       to=topic_author_email,
                       subject="There is new comment on your topic: %s" % topic_title,
                       body="""Your topic: {0} received a new comment.

                       Click <a href="http://your-domain.org/topic/{1}">on this link</a> to see it""".format(topic_title,
                                                                                                             topic_id))
