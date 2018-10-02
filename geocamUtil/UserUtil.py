# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
# __END_LICENSE__

from django.contrib.auth.models import User


def user_exists(first_name, last_name):
    existing_users = User.objects.filter(first_name=first_name, last_name=last_name)
    return existing_users.count() > 0


def username_exists(username):
    existing_users = User.objects.filter(username=username)
    return existing_users.count() > 0


def get_new_username_from_name(first_name, last_name):
    if last_name:
        # Username is first initial plus last name in lower case
        username = first_name[0].lower() + last_name.lower()
    else:
        username = first_name.lower()

    if username_exists(username):
        user_uniquifier = 1
        while username_exists(username):
            username = first_name[0].lower() + last_name.lower() + '%s' % user_uniquifier
            user_uniquifier += 1

    return username


def create_user(first_name, last_name, save=True, verbose=False, force_create=False):
    """
    Creates a user, with a unique username
    :param first_name:
    :param last_name:
    :param save: save the new user record
    :param verbose: prints a message if user exists
    :param force_create: true to force creation of a newly named user
    :return: the user record, or None if force_create is false.
    """
    if user_exists(first_name, last_name):
        if verbose:
            print 'User named "%s %s" already exists' % (first_name, last_name)
        if not force_create:
            return None

    username = get_new_username_from_name(first_name, last_name)

    # Now we should have a unique username and a need to create the user
    user_data = {'first_name': first_name,
                 'last_name': last_name,
                 'username': username,
                 'password': "*",
                 'is_active': False,
                 'is_superuser': False}

    new_user = User(**user_data)
    if save:
        new_user.save()
    return new_user


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
    try:
        return User.objects.get(first_name=first, last_name=last)
    except:
        try:
            # try lowercase search
            found_users = User.objects.filter(first_name__icontains=first.lower(), last_name__icontains=last.lower())
            return found_users.first()
        except:
            pass
        return None


def getUserByUsername(username):
    try:
        return User.objects.get(username=username.lower())
    except:
        return None