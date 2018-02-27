from __future__ import print_function
import os

from judge.models import Submission, Contest, SUBMISSION_RESULT, ContestParticipation


def create_user_dir(contest_key, username):
    prefix = '/vagrant/sources/%s' % contest_key
    dirname = '%s/%s' % (prefix, username)
    if not os.path.exists(dirname):
        os.makedirs(dirname)


def write_source(username, filename, source, contest_key):
    prefix = '/vagrant/sources/%s' % contest_key
    dirname = '%s/%s' % (prefix, username)
    filepath = '%s/%s' % (dirname, filename)
    f = open(filepath, 'w')
    print(source, file=f)


def down(contest_key):
    # contest_key = "dn1711e2"
    # from pprint import pprint
    # contest = Contest.objects.filter(key=contest_key).first()
    #
    # pprint(vars(contest))
    for participation in ContestParticipation.objects.filter(contest__key=contest_key):
        submissions = participation.submissions.all()
        for contest_submission in submissions:
            submission = contest_submission.submission
            # pprint(vars(submission))
            create_user_dir(contest_key, submission.user)
            filename = '%s-%s.txt' % (submission.problem.code, submission.id)
            write_source(submission.user, filename, submission.source, contest_key)
        print(len(submissions))
