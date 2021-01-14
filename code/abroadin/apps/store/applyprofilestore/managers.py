from django.db.models import QuerySet

from abroadin.apps.applyprofile.models import ApplyProfile


class ApplyProfileGroupManager(QuerySet):

    def create_by_ap_ids(self, **kwargs):
        apply_profile_ids = kwargs.pop('apply_profile_ids')
        obj = self.create(**kwargs)
        apply_profiles = list(ApplyProfile.objects.filter(id__in=apply_profile_ids))
        obj.apply_profiles.set(apply_profiles)