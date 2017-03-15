import datetime

from handlers.base import BaseHandler
from models.comment import Comment


class DeleteCommentsCron(BaseHandler):
    def get(self):

        # fetch comments older tahn 30 days from DataStore
        deleted_comments = Comment.query(Comment.deleted == True,
                                         Comment.updated < datetime.datetime.now() - datetime.timedelta(days=30)).fetch()

        for comment in deleted_comments:
            comment.key.delete()
