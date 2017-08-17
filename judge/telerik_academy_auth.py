from django.contrib.auth.backends import RemoteUserBackend

from django.contrib.auth.models import User

import requests

from judge.models import Profile, Language

class RemoteUserBackend (object):
    def authenticate(self, username=None, password=None):
        # Telerik Academy Authentication

        r = requests.post('http://best.telerikacademy.com/api/users/login', data = {
            'grant_type': 'password',
            'username': username,
            'password': password,
        })

        import pdb; pdb.set_trace()

        if r.status_code == requests.codes.ok:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User(username=username)
                user.password = '123456qw'
                user.is_staff = True
                user.is_superuser = True
                user.save()

                profile, _ = Profile.objects.get_or_create(user=user, defaults={
                    'language': Language.get_python2(),
                    'timezone': 'Europe/Sofia',
                })

                profile.name = username
                profile.save()
            return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None







