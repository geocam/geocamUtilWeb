# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
# __END_LICENSE__

from django.contrib.auth.models import User

def getUserName(user):
    if not user:
        return ''
    username = user.username
    if user.first_name:
        username = user.first_name
        if user.last_name:
            username = username + " " + user.last_name
    return username


def getUserByNames(first, last):
    return User.objects.get(first_name=first, last_name=last)


def getUserByUsername(username):
    return User.objects.get(username=username)