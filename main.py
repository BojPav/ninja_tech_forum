#!/usr/bin/env python
import webapp2
from handlers.base import MainHandler, AboutHandler, CookieHandler, UserCommentsHandler
from handlers.topics import TopicCreateHandler, TopicDetailsHandler, TopicDeleteHandler
from handlers.comments import CommentAdd
from workers.email_new_comment import EmailNewCommentWorker

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="main-page"),
    webapp2.Route('/about', AboutHandler, name="about-page"),
    webapp2.Route('/set-cookie', CookieHandler, name="set-cookie"),
    webapp2.Route('/topic/create', TopicCreateHandler, name="topic-create"),
    webapp2.Route('/topic/<topic_id:\d+>', TopicDetailsHandler, name="topic-details"),
    webapp2.Route('/topic/<topic_id:\d+>/delete', TopicDeleteHandler, name="topic-delete"),
    webapp2.Route('/topic/<topic_id:\d+>/comment/add', CommentAdd, name="comment-add"),
    webapp2.Route('/user-comments', UserCommentsHandler, name="user-comments"),
    # tasks
    webapp2.Route('/task/email-new-comment', EmailNewCommentWorker, name="task-email-new-comment"),
], debug=True)
