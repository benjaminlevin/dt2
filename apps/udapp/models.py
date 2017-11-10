# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import bcrypt, re # bcrypt + regex
from django.contrib import messages # flash messages
from datetime import datetime, date, timedelta # datetime
import pytz # for time comparison
from ..login_registration.models import User # from login_registration app

class MessageReplyManager(models.Manager):
    
    # for both messages and replies
    def validate(self, request):
        post_data = request.POST
        data_check = True
        if len(post_data['content']) < 1:
            data_check = False
            messages.info(request, 'message and reply content must be more than zero characters')
        if len(post_data['content']) > 500:
            data_check = False
            messages.info(request, 'message and reply content may not be longer than 500 characters')
        return data_check

    def create_message(self, request, rid, aid):
        post_data = request.POST
        try:
            recipient = User.objects.get_user(rid)[1]
            author = User.objects.get_user(aid)[1]
            Message.objects.create(
                content = post_data['content'],
                author = author,
                recipient = recipient,
            )
        except:
            pass
        return self
        
    def create_reply(self, request, mid, aid):
        post_data = request.POST
        try:
            message = Message.objects.get(id=mid)
            author = User.objects.get_user(aid)[1]
            Reply.objects.create(
                content = post_data['content'],
                author = author,
                message = message,
            )
        except:
            pass
        return self

    def get_messages_by_recipient(self, rid):
        recipient =  User.objects.get_user(rid)[1]
        messages = Message.objects.filter(recipient = recipient).order_by('-created_at')
        # checking for messages
        if len(messages) > 0:
            now = datetime.now(pytz.timezone('America/Chicago'))
            for message in messages:
                # rendering 'time past' data for message
                created_at = message.created_at
                time = (now - created_at)
                # default date format
                message.time_past = str(created_at.strftime('%B %d, %Y'))
                message.time = " "
                # less than one week
                if ((time.seconds)/((60*60)*7)) < 7:
                    message.time_past = ((time.seconds)/((60*60)*7))
                    message.time = " days ago"
                    if message.time_past == 1:
                        message.time = " day ago"
                # less than one day
                if ((time.seconds)/(60*60)) < 24:
                    message.time_past = ((time.seconds)/(60*60))
                    message.time = " hours ago"
                    if message.time_past == 1:
                        message.time = " hour ago"
                # less than one hour
                if ((time.seconds)/60) < 60:
                    message.time_past = (time.seconds)/(60)
                    message.time = " minutes ago"
                    if message.time_past == 1:
                        message.time = " minute ago"
                # checking for message replies
                message.reply_messages = Reply.objects.filter(message = message).order_by('created_at')
                if len(message.reply_messages) > 0:
                    # rendering 'time past' data for reply
                    for reply in message.reply_messages:
                        created_at = reply.created_at
                        time = (now - created_at)
                        # default date format
                        reply.time_past = str(created_at.strftime('%B %d, %Y'))
                        reply.time = " "
                        # less than one week
                        if ((time.seconds)/((60*60)*7)) < 7:
                            reply.time_past = ((time.seconds)/((60*60)*7))
                            reply.time = " days ago"
                            if reply.time_past == 1:
                                reply.time = " day ago"
                        # less than one day
                        if ((time.seconds)/(60*60)) < 24:
                            reply.time_past = (time.seconds)/(60*60)
                            reply.time = " hours ago"
                            if reply.time_past == 1:
                                reply.time = " hour ago"
                        # less than one hour
                        if ((time.seconds)/60) < 60:
                            reply.time_past = ((time.seconds)/60)
                            reply.time = " minutes ago"
                            if reply.time_past == 1:
                                reply.time = " minute ago"
        return messages

    # specific for finding recipient id (create_reply() POST handling)        
    def recipient_id(self, mid):
        data_check = False
        try:
            message = Message.objects.get(id=mid)
            rid = message.recipient.id
            data_check = True
        except:
            rid = 0
        return data_check, rid

class Message(models.Model):
    content = models.CharField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_sent')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_received')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MessageReplyManager()

class Reply(models.Model):
    content = models.CharField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replies')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MessageReplyManager()