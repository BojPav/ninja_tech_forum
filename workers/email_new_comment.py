from handlers.base import BaseHandler
from google.appengine.api import mail


class EmailNewCommentWorker(BaseHandler):
    def post(self):
        topic_author_email = self.request.get("topic_author_email")
        topic_title = self.request.get("topic_title")
        comment_content = self.request.get("comment_content")

        # send mail
        mail.send_mail(sender="pavlovicbojan86@gmail.com",
                       to=topic_author_email,
                       subject="There is new comment on your topic: %s !" % topic_title,
                       body="Comment: %s" % comment_content)
