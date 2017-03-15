import datetime

from google.appengine.api import mail

from handlers.base import BaseHandler
from models.subscribe import Subscriber
from models.topic import Topic


class SubsTopicsCron(BaseHandler):
    def get(self):

        # get topics in last 24h
        topics = Topic.query(Topic.deleted == False,
                             Topic.updated < datetime.datetime.now() - datetime.timedelta(days=1)).fetch()

        # get subscribed emails
        emails = Subscriber.query(Subscriber.deleted == False).fetch()

        for topic in topics:
            for email in emails:
                mail.send_mail(sender="pavlovicbojan86@gmail.com",
                               to=email.subscribe_email,
                               subject="New topics on Ninja Tech Forum !",
                               body="""Check out...{0}""".format(topic.title))
