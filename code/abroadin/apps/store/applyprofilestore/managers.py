from django.db.models import QuerySet

from abroadin.apps.applyprofile.models import ApplyProfile

from .validators import validate_apply_profiles


class ApplyProfileGroupManager(QuerySet):

    def create_by_apply_profiles(self, **kwargs):
        apply_profiles = kwargs.pop('apply_profiles')
        apply_profiles = validate_apply_profiles(apply_profiles)
        obj = self.create(**kwargs)
        obj.apply_profiles.set(apply_profiles)
        return obj
