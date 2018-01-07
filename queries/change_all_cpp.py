from judge.models import Submission, Language


def update_all_to_latest_cpp():
    cpp03 = Language.objects.filter(name="C++03")[0]
    cpp11 = Language.objects.filter(name="C++11")[0]
    cpp14 = Language.objects.filter(name="C++ 14")[0]
    cpp = Language.objects.filter(name="C++")[0]

    Submission.objects.filter(language=cpp03) \
        .update(language=cpp)
    Submission.objects.filter(language=cpp11) \
        .update(language=cpp)
    Submission.objects.filter(language=cpp14) \
        .update(language=cpp)
