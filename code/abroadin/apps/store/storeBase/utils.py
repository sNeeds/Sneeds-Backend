import abroadin.apps.users.consultants.models
import abroadin.apps.users.customAuth.models


def is_consultant(user):
    if abroadin.apps.users.consultants.models.ConsultantProfile.objects.filter(user__exact=user).exists():
        return True
    return False
