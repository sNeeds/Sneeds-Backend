from abroadin.apps.applyprofile.models import ApplyProfile


def get_user_bought_apply_profiles(user):
    return ApplyProfile.objects.filter(soldapplyprofilegroup__sold_to=user).distinct()
