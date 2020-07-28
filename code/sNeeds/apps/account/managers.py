from django.db import models, transaction

from sNeeds.apps.account.models import Grade


class UniversityThroughQuerySetManager(models.QuerySet):
    def get_bachelors(self):
        return self.all().filter(grade=Grade.BACHELOR)

    def get_masters(self):
        return self.all().filter(grade=Grade.MASTER)

    def get_phds(self):
        return self.all().filter(grade=Grade.PHS)

    def get_post_docs(self):
        return self.all().filter(grade=Grade.POST_DOC)
