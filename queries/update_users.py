import json
import string
import urllib

import requests
from django.contrib.auth.models import User
from django.db.backends.mysql.base import IntegrityError

from dmoj import settings
from judge.models import Profile, Language


def get_url(users):
    users_string = json.dumps([user.username for user in users])

    url = "https://my.telerikacademy.com/api/users/userinfos?apiKey=%s&usernames=%s" % (
        settings.API_KEY, users_string)
    return url


def update_users(group_size=10):
    # group_size = 50
    users = User.objects.all()
    users_by_username = {}
    for user in users:
        users_by_username[user.username] = user

    i = 0
    groups = [[]]
    while i < len(users):
        if len(groups[-1]) >= group_size:
            groups.append([])
        if not users[i].email:
            groups[-1].append(users[i])
        i += 1
    missing = []
    group_index = 0
    for group in groups:
        group_index += 1
        print(group_index)
        url = get_url(group)
        response = requests.get(url)
        users_dicts = json.loads(response.content)
        user_dicts_by_username = {}
        for user_dict in users_dicts:
            user_dicts_by_username[user_dict["Username"]] = user_dict

        for username in [x.username for x in group]:
            if username not in user_dicts_by_username:
                missing.append(username)
            else:
                email = user_dicts_by_username[username]['Email']
                if not email:
                    print(username, user_dicts_by_username[username])
                    continue
                user = users_by_username[username]
                user.email = email
                user.username = ''.join(x for x in email if x.isalnum() or x == '_')
                print(user.username)
                profile, _ = Profile.objects.get_or_create(user=user, defaults={
                    'language': Language.get_python2(),
                    'timezone': 'Europe/Sofia',
                })

                profile.name = email[:email.index('@')]

                profile.avatar = user_dicts_by_username[username]['ProfileAvatarUrl']
                profile.save()
                try:
                    user.save()
                except:
                    print(username)
                    # print(found)
                    # print(missing)
                    # print(found)
        print(missing)
