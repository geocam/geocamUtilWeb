# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

from settings import INVITE_SUBJECT, INVITE_FROM, INVITE_MESSAGE

from django.core.mail import send_mail, BadHeaderError
from django.contrib.sites.models import Site
from django.contrib.auth.models import User

from geocamCore.models import GroupInvite

import datetime

def send_email(to_email, from_email, subject, message):
    succesful = False
    
    # Make sure that our email has all the parts it needs
    if subject and message and from_email:
        
        # Make sure that we're not sending invalid headers
        try:
            
            send_mail(subject, message, from_email, [to_email])
            succesful = True
            
        except BadHeaderError:
            pass
    
    return succesful


def format_and_send_invite_email(to_email, group_name, join_link=None, from_email=None, subject=None, message=None):
    """
    The from_email, subject and message are provided as arugments as well
    as settings so that they can be overridden in the case of special 
    invite situtations, (ie: resending or senitive invites)
    """
    
    if subject == None:
        subject = INVITE_SUBJECT
    
    if from_email == None:
        from_email = INVITE_FROM
        
    if message == None:
        message = INVITE_MESSAGE
        
    if join_link == None:
        import urllib
        join_link = invite_link = 'http://127.0.0.1:8000/manage/groups/join/?group=%s' % urllib.urlencode(group_name)
        
    # Subject, from_email and message can all be formatted strings
    # that we will auto fill with some basic values
    basic_values = dict(groupname=group_name, invitelink=join_link)
     
    subject = subject % basic_values
    message = message % basic_values
     
    return send_email(to_email, from_email, subject, message)

    
def send_group_invites(group, member_list, join_link, password_required=False):
    count = 0
    
    for member in member_list:
        email = member.replace(",", "")
        
        # Create the Group Invite Record
        invite = GroupInvite()

        invite.group = group
        invite.email = email
        invite.redeemed
        invite.password_required = password_required

        # Check to see if there is a user for this
        try:
            invite.user = User.objects.get(email=member)
            invite.existing_user = True
        # If the user doesn't exist we'll make a note
        except User.DoesNotExist:
            invite.user = None
            invite.existing_user = False

        invite.sent_successfully = format_and_send_invite_email(email, group.name, join_link)
        invite.send = datetime.datetime.now() 
        invite.save()

        # If the invite was sent succesfully then increase the send count
        if invite.sent_successfully == True:
            count = count + 1
        
    return count
