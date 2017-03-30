#!/usr/bin/env python
import webapp2

from crons.delete_comments import DeleteCommentsCron
from crons.delete_topics_cron import DeleteTopicsCron
from crons.send_topics_subscribers import SubsTopicsCron
from handlers.base import MainHandler, AboutHandler, CookieHandler, UserCommentsHandler
from handlers.gallery import GalleryHandler
from handlers.subscribers import SubscribeHandler
from handlers.topics import TopicCreateHandler, TopicDetailsHandler, TopicDeleteHandler
from handlers.comments import CommentAdd, CommentDelete
from workers.email_new_comment import EmailNewCommentWorker

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="main-page"),
    webapp2.Route('/about', AboutHandler, name="about-page"),
    webapp2.Route('/set-cookie', CookieHandler, name="set-cookie"),

    # topics
    webapp2.Route('/topic/create', TopicCreateHandler, name="topic-create"),
    webapp2.Route('/topic/<topic_id:\d+>', TopicDetailsHandler, name="topic-details"),
    webapp2.Route('/topic/<topic_id:\d+>/delete', TopicDeleteHandler, name="topic-delete"),

    # comments
    webapp2.Route('/topic/<topic_id:\d+>/comment/add', CommentAdd, name="comment-add"),
    webapp2.Route('/user-comments', UserCommentsHandler, name="user-comments"),
    webapp2.Route('/comment/<comment_id:\d+>/delete', CommentDelete, name="comment-delete"),

    # gallery
    webapp2.Route('/gallery', GalleryHandler, name="gallery"),

    # subscribe
    webapp2.Route('/topic-subscribe', SubscribeHandler, name="topic-subscribe"),

    # cron
    webapp2.Route("/cron/delete-topics", DeleteTopicsCron, name="cron-delete-topics"),
    webapp2.Route("/cron/subs-topics", SubsTopicsCron, name="subs-topic-cron"),
    webapp2.Route("/cron/delete-comments", DeleteCommentsCron, name="cron-delete-comments"),

    # workers
    webapp2.Route('/task/email-new-comment', EmailNewCommentWorker, name="task-email-new-comment"),
], debug=True)
