# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse # HttpResponse not in use
# importing user model from login_registration app
from ..login_registration.models import User
from .models import Message, Reply

def create(request):
    # if user is not logged in
    if 'id' not in request.session:
        return redirect('/')
    # if user is not admin
    if request.session['level'] != 9:
        return redirect('/')
    if request.method == 'GET':
        return render(request, 'udapp/create.html')
    if request.method == 'POST':
        if User.objects.validate_new(request) is True:
            User.objects.register_new(request)
            return redirect('/dashboard/admin')
        return redirect('/users/new')

def edit(request, **uid): #include redirect if not admin
    # if user is not logged in
    if 'id' not in request.session:
        return redirect('/')
    # convert kwarg to integer
    if uid:
        uid = uid['uid']
    if not uid:
        uid = request.session['id']
    if request.method == 'GET':
        # if user is not authorized for entered user id
        if int(request.session['id']) == int(uid) or int(request.session['level']) == 9:
            user = User.objects.get_user(uid)
            # if user found
            if user[0] is True:
                user = user[1]
                context = {
                    'user' : user
                }
                return render(request, 'udapp/edit.html', context)
        return redirect('/dashboard')
    if request.method == 'POST':
        # if user found
        if User.objects.validate_edit(request) is True:
            User.objects.edit(request, uid)
        return redirect('/users/edit/' + uid)

def edit_description(request, uid):
    # if user is not logged in
    if 'id' not in request.session:
        return redirect('/')
    # if user is not authorized for entered user id
    if int(request.session['id']) != int(uid):
        return redirect('/')
    if request.method == 'POST':
        if User.objects.validate_description(request) is True:
            User.objects.edit_description(request, uid) 
    return redirect('/users/edit/' + uid)

def edit_password(request, uid):
    if request.method == 'POST':
        # if user is not authorized for entered user id
        if request.session['level'] != 9 and request.session['id'] != uid:
            return redirect('/')
        if User.objects.validate_password(request) is True:
            User.objects.edit_password(request, uid)
    return redirect('/users/edit/' + uid)

def remove(request, uid):
    # if user is not logged in
    if 'id' not in request.session:
        return redirect('/')
    # if user is not authorized for entered user id
    if int(request.session['level']) != int(9) and int(request.session['id']) != int(uid):
        return redirect('/')
    if request.method == 'GET':
        if User.objects.get_user(uid)[0] is True:
            context = {
                'user' : User.objects.get_user(uid)[1]
            }
            return render(request, 'udapp/remove.html', context)
        return redirect('/dashboard')
    if request.method == 'POST':
        User.objects.remove_user(uid)
        return redirect('/dashboard')

def show(request, uid):
    # if user is not logged in
    if 'id' not in request.session:
        return redirect('/')
    if User.objects.get_user(uid)[0] is True:
        user = User.objects.get_user(uid)[1]
        user_messages = Message.objects.get_messages_by_recipient(uid)
        context = {
            'user' : user,
            'user_messages' : user_messages
        }
        return render(request, 'udapp/user.html', context)
    return redirect('/dashboard')

def create_message(request, rid, aid):
    if 'id' not in request.session:
        return redirect('/')
    if int(aid) != int(request.session['id']):
        return redirect('/dashboard')
    if request.method == 'POST':
        if Message.objects.validate(request) is True:
            Message.objects.create_message(request, rid, aid)
    return redirect('/users/show/' + rid)

def create_reply(request, mid, aid):
    if 'id' not in request.session:
        return redirect('/')
    if int(aid) != request.session['id']:
        return redirect('/dashboard')
    if request.method == 'POST':
        if Reply.objects.recipient_id(mid)[0] is True:
            rid = int(Reply.objects.recipient_id(mid)[1])
            if Reply.objects.validate(request) is True:
                Reply.objects.create_reply(request, mid, aid)
            return redirect('/users/show/' + str(rid))
    return redirect('/dashboard')
    