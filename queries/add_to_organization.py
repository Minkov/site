import datetime

from judge.models.profile import Profile, Organization, OrganizationRequest


def add_to_org(organisation_key, usernames_string):
    organisation = Organization.objects.filter(key=organisation_key).first()
    print(organisation)
    usernames = usernames_string.split(',')
    profiles = Profile.objects.filter(user__username__in=usernames)

    def create_org_request(user, org):
        request = OrganizationRequest(user=user, organization=org, state="P", time=datetime.datetime.now())
        return request

    requests = map(lambda user: create_org_request(user, organisation), profiles)

    # for profile in profiles:
    #     profile.organizations.all().append(organisation)
    #     print(profile.organizations.all())

    for req in requests:
        req.save()
