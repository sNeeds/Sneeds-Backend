import sNeeds.apps.users.consultants.models
import sNeeds.apps.users.customAuth.models


def is_consultant(user):
    if sNeeds.apps.users.consultants.models.ConsultantProfile.objects.filter(user__exact=user).exists():
        return True
    return False
