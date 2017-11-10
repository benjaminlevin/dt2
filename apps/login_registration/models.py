# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import bcrypt, re # bcrypt + regex
from django.contrib import messages # flash messages
from datetime import datetime, date, timedelta #datetime

class UserManager(models.Manager):
    
    # Login + Registration
    
    def validate(self, request):
        post_data = request.POST
        data_check = True
        if len(post_data['first_name']) < 2:
            data_check = False
            messages.error(request, 'first name must contain two or more characters')
        if re.match('^([A-Za-z]+\s)*[A-Za-z]*$', post_data['first_name']) is None:
            data_check = False
            messages.error(request, 'first name may only contain letters')
        if len(post_data['last_name']) < 2:
            data_check = False
            messages.error(request, 'last name must contain two or more characters')
        if re.match('^([A-Za-z]+\s)*[A-Za-z]*$', post_data['last_name']) is None:
            data_check = False
            messages.error(request, 'last name may only contain letters')
        if re.match('^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$', post_data['email']) is None:
            data_check = False
            messages.error(request, 'e-mail must be valid')
        if len(User.objects.filter(email=post_data['email'])) > 0:
            data_check = False
            messages.error(request, 'e-mail address already registered')
        # convert date and now values for comparison
        try:
            dob = datetime.strptime(post_data['birthday'], '%Y-%m-%d').date()
            now = datetime.now().date()
            if  dob > now:
                data_check = False
                messages.error(request, 'date of birth may not occur before today')
            if  (dob.year + 100) < now.year:
                data_check = False
                messages.error(request, 'you are too old, go take a nap')
        except:
            data_check = False
            messages.error(request, 'invalid date of birth entry')
        if len(post_data['password']) < 8:
            data_check = False
            messages.error(request, 'password must contain eight or more characters')
        if post_data['password'] != post_data['confirm_password']:
            data_check = False
            # 'error' tag messages for registration validation
            messages.error(request, 'passwords must match')
        return data_check

    def register(self, request):
        post_data = request.POST
        # encode and convert entered data
        password = post_data['password'].encode(encoding='utf-8', errors='strict')
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        birthday =  datetime.strptime(post_data['birthday'], "%Y-%m-%d").date()
        # check if this is the first user
        dbcheck = len(User.objects.all())
        if dbcheck == 0:
            # create admin user
            User.objects.create(
                first_name = post_data['first_name'],
                last_name = post_data['last_name'],
                email = post_data['email'],
                password = hashed,
                birthday = birthday,
                level = 9,
                ) 
        elif dbcheck != 0:
            # create default user
            User.objects.create(
                first_name = post_data['first_name'],
                last_name = post_data['last_name'],
                email = post_data['email'],
                password = hashed,
                birthday = birthday,
                level = 5,
                ) 
        return self

    def login(self, request):
        post_data = request.POST
        data_check = False 
        # check db for email 
        user = User.objects.filter(email=post_data['email']) 
        if len(user) > 0: 
            # fetch user data
            user = User.objects.get(email=post_data['email'])
            # compare entered and stored passwords
            password = post_data['password'].encode(encoding='utf-8', errors='strict')
            stored = User.objects.get(email=post_data['email']).password.encode(encoding='utf-8', errors='strict')
            if bcrypt.checkpw(password, stored) is True:
                data_check=True
                # set session data
                request.session['id'] = user.id
                request.session['first_name'] = user.first_name
                request.session['level'] = user.level  
                return data_check, request
        # invalid login
        # 'warning' tag messages for login
        messages.warning(request, 'Invalid login')
        return data_check, request

# Added Functions

    def get_user(self, uid):
        data_check = False 
        # check db for id 
        user = User.objects.filter(id=uid) 
        if len(user) > 0: 
            # fetch user data
            user = User.objects.get(id=uid)
            if user.birthday:
                birthday =  user.birthday
                user.birthday =  birthday.strftime('%Y-%m-%d')
                user.form_birthday = birthday.strftime('%B %d, %Y')
            user.created_at = user.created_at.strftime('%B %d, %Y')
            data_check = True
        return data_check, user

    def render_users(self):
        users = User.objects.all()
        # PLAYING
        # users = User.objects.raw('SELECT * FROM login_registration_User WHERE ID=7;')
        # users = User.objects.raw('SELECT * FROM login_registration_User;') #next functions don't work with raw query
        for user in users:
            if user.level == 9:
                user.user_level = 'admin'
            elif user.level != 9:
                user.user_level = 'normal'
            user.created_at = user.created_at.strftime('%B %d, %Y')
        return users

# Create New User

    def validate_new(self, request):
        post_data = request.POST
        data_check = True
        if re.match('^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$', post_data['email']) is None:
            data_check = False
            messages.error(request, 'e-mail must be valid')
        if len(User.objects.filter(email=post_data['email'])) > 0:
            data_check = False
            messages.error(request, 'e-mail address already registered')
        if len(post_data['first_name']) < 2:
            data_check = False
            messages.error(request, 'first name must contain two or more characters')
        if re.match('^([A-Za-z]+\s)*[A-Za-z]*$', post_data['first_name']) is None:
            data_check = False
            messages.error(request, 'first name may only contain letters')
        if len(post_data['last_name']) < 2:
            data_check = False
            messages.error(request, 'last name must contain two or more characters')
        if re.match('^([A-Za-z]+\s)*[A-Za-z]*$', post_data['last_name']) is None:
            data_check = False
            messages.error(request, 'last name may only contain letters')
        if len(post_data['password']) < 8:
            data_check = False
            messages.error(request, 'password must contain eight or more characters')
        if post_data['password'] != post_data['confirm_password']:
            data_check = False
            # 'error' tag messages for new user validation
            messages.error(request, 'passwords must match')
        return data_check

    def register_new(self, request):
        post_data = request.POST
        # encode and convert entered data
        password = post_data['password'].encode(encoding='utf-8', errors='strict')
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        User.objects.create(
            first_name = post_data['first_name'],
            last_name = post_data['last_name'],
            email = post_data['email'],
            password = hashed,
            level = 5,
            ) 
        return self

    # Edit User Info

    def validate_edit(self, request):
        post_data = request.POST
        data_check = True
        if re.match('^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$', post_data['email']) is None:
            data_check = False
            messages.error(request, 'e-mail must be valid')
        if len(User.objects.filter(email=post_data['email'])) > 1:
            data_check = False
            messages.error(request, 'e-mail address already registered')
        if len(post_data['first_name']) < 2:
            data_check = False
            messages.error(request, 'first name must contain two or more characters')
        if re.match('^([A-Za-z]+\s)*[A-Za-z]*$', post_data['first_name']) is None:
            data_check = False
            messages.error(request, 'first name may only contain letters')
        if len(post_data['last_name']) < 2:
            data_check = False
            messages.error(request, 'last name must contain two or more characters')
        if re.match('^([A-Za-z]+\s)*[A-Za-z]*$', post_data['last_name']) is None:
            data_check = False
            messages.error(request, 'last name may only contain letters')
        # convert date and now values for comparison
        try:
            dob = datetime.strptime(post_data['birthday'], '%Y-%m-%d').date()
            now = datetime.now().date()
            if  dob > now:
                data_check = False
                messages.error(request, 'date of birth may not occur before today')
            if  (dob.year + 100) < now.year:
                data_check = False
                messages.error(request, 'you are too old, go take a nap')
        except:
            data_check = False
            messages.error(request, 'invalid date of birth entry')
        return data_check

    def edit(self, request, uid):
        post_data = request.POST
        data_check = False 
        # check db for id 
        user = User.objects.filter(id=uid) 
        if len(user) > 0: 
            # fetch user data
            user = User.objects.get(id=uid)
            birthday =  datetime.strptime(post_data['birthday'], "%Y-%m-%d").date()
            user.first_name = post_data['first_name']
            user.last_name = post_data['last_name']
            user.email = post_data['email']
            user.birthday = birthday
            user.level = post_data['level']
            user.save()
            # refresh of credentials for signed in user
            if user.id == request.session['id']:
                user = User.objects.get(id=request.session['id'])
                request.session['first_name'] = user.first_name
                request.session['level'] = user.level
        return self

    # Edit Description

    def validate_description(self, request):
        post_data = request.POST
        data_check = True
        if len(post_data['description']) > 500:
            data_check = False
            messages.info(request, 'description may not be longer than 500 characters')
        return data_check

    def edit_description(self, request, uid):
        post_data = request.POST
        user = User.objects.filter(id=uid) 
        if len(user) > 0: 
            user = User.objects.get(id=uid)
            user.description = post_data['description']
            user.save()
        return self

    # Edit Password

    def validate_password(self, request):
        post_data = request.POST
        data_check = True
        if len(post_data['password']) < 8:
            data_check = False
            # 'warning' tag messages
            messages.warning(request, 'password must contain eight or more characters')
        if post_data['password'] != post_data['confirm_password']:
            data_check = False
            # 'warning' tag messages
            messages.warning(request, 'passwords must match')
        return data_check

    def edit_password(self, request, uid):
        post_data = request.POST
        password = post_data['password'].encode(encoding='utf-8', errors='strict')
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        user = User.objects.filter(id=uid) 
        if len(user) > 0: 
            user = User.objects.get(id=uid)
            user.password = hashed
            user.save()
        return self

# Delete User

    def remove_user(self, uid):
        try:
            user = User.objects.get(id=uid)
            user.delete()
            print 'deleted'
        except:
            pass
        return self

# Development

    def cleardb(self):
        # # delete all users
        # User.objects.all().delete()
        return self

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    birthday = models.DateField(auto_now=False, auto_now_add=False, null=True)
    level = models.IntegerField()
    description = models.CharField(max_length=500, default=' ')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
