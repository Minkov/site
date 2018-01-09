from judge.models import Submission, Language

def get_all_users_with_lang():
    language = Language.objects.filter(name="Java").first()

    usernames = map(lambda x: x['user__name'], Submission.objects.filter(language=language).values('user__name'))
    usernames = sorted(list(set(usernames)))
    for username in usernames:
        print(username)