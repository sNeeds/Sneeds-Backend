from django.db import models, transaction


class UniversityThroughQuerySetManager(models.QuerySet):

    def get_bachelor(self):
        from sNeeds.apps.account.models import Grade
        try:
            return self.all().get(grade=Grade.BACHELOR)
        except self.model.DoesNotExist:
            return None

    def get_master(self):
        from sNeeds.apps.account.models import Grade
        try:
            return self.all().filter(grade=Grade.MASTER)
        except self.model.DoesNotExist:
            return None

    def get_phd(self):
        from sNeeds.apps.account.models import Grade
        try:
            return self.all().filter(grade=Grade.PHD)
        except self.model.DoesNotExist:
            return None

    def get_post_doc(self):
        from sNeeds.apps.account.models import Grade
        try:
            return self.all().filter(grade=Grade.POST_DOC)
        except self.model.DoesNotExist:
            return None
