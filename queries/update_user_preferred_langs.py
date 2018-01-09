from judge.models import Profile, Language, Submission

def get_user_preferred_language(profile):
    user_languages = map(lambda x: x["language"],
                         Submission.objects.filter(user=profile).values('language').values('language'))

    if len(user_languages) is 0:
        return Language.objects.filter(name="Python 3").first()

    submissions_count_by_lang = {}
    for user_lang in user_languages:
        if user_lang not in submissions_count_by_lang:
            submissions_count_by_lang[user_lang] = 0
        submissions_count_by_lang[user_lang] += 1

    preferred_lang = user_languages[0]
    preferred_lang_count = submissions_count_by_lang[preferred_lang]

    for lang, count in submissions_count_by_lang.iteritems():
        if preferred_lang_count < count:
            preferred_lang = lang
            preferred_lang_count = count
    return Language.objects.filter(id=preferred_lang).first()

def update_preferred_langs():
    for profile in Profile.objects.all():
        profile.language = get_user_preferred_language(profile)
        profile.save()