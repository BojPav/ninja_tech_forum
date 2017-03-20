import datetime

from google.appengine.api import mail

from handlers.base import BaseHandler
from models.subscribe import Subscriber
from models.topic import Topic


class SubsTopicsCron(BaseHandler):
    def get(self):

        # get latest topics
        topics_latest = Topic.query(Topic.deleted == False,
                             Topic.updated > datetime.datetime.now() - datetime.timedelta(days=1)).fetch()

        # get subscribed emails
        subscribers_emails = Subscriber.query(Subscriber.deleted == False).fetch()

        if topics_latest:
            topic_links = ""
            for topic in topics_latest:
                topic_links += topic.title + ">> " + "http://bojpav-ninjatech-forum.appspot.com/topic/" + str(topic.key.id()) + "<< "

            for email in subscribers_emails:
                mail.send_mail(sender="pavlovicbojan86@gmail.com",
                               to=email.subscribe_email,
                               subject="New topics on Ninja Tech Forum in last 24h !",
                               body="Check out: %s" % topic_links)
