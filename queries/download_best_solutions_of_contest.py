from __future__ import print_function
import os


from judge.models import Submission, Contest, SUBMISSION_RESULT

def create_user_dir(username):
    prefix = '/vagrant/sources'
    dirname = '%s/%s' % (prefix, username)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

def write_source(username, filename, source):
    prefix = '/vagrant/sources'
    dirname = '%s/%s' % (prefix, username)
    filepath = '%s/%s' % (dirname, filename)
    f = open(filepath, 'w')
    print(source, file=f)

def down(contest_key):
    submissions = [submission for submission in Submission.objects.filter(result="AC")
                   if submission.contest_or_none and submission.contest_key == contest_key]

    for sub in submissions:
        create_user_dir(sub.user)
        filename = '%s-%s.cs' % (sub.problem.code, sub.id)
        write_source(sub.user, filename, sub.source)
    print(len(submissions))
