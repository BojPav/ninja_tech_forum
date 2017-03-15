from handlers.base import BaseHandler
# from google.appengine.api import users
from utils.decorators import validate_csrf
from models.subscribe import Subscriber


class SubscribeHandler(BaseHandler):
    def get(self):
        return self.render_template_with_csrf("subscribe_user.html")

    @validate_csrf
    def post(self):

        # check if user is logged in
        # user = users.get_current_user()
        # if not user:
            # return self.write("Please login, not allowed for unregistered users to post a topic...!")

        # get subscribers mail
        subscribe_email = self.request.get("subscription_email")

        # put email in Datastore
        Subscriber.create(subscribe_email=subscribe_email)

        return self.redirect_to("main-page")
