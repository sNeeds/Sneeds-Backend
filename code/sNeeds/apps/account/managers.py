from django.db import models, transaction


class UniversityThroughQuerySetManager(models.QuerySet):

    def get_bachelors(self):
        from sNeeds.apps.account.models import Grade

        return self.all().filter(grade=Grade.BACHELOR)

    def get_masters(self):
        from sNeeds.apps.account.models import Grade

        return self.all().filter(grade=Grade.MASTER)

    def get_phds(self):
        from sNeeds.apps.account.models import Grade

        return self.all().filter(grade=Grade.PHS)

    def get_post_docs(self):
        from sNeeds.apps.account.models import Grade

        return self.all().filter(grade=Grade.POST_DOC)
