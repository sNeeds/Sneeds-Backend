from django.contrib.contenttypes.models import ContentType


class TestFixtureMixIn:

    # def __init__(self):
    #     self.setUp()

    def setUp(self) -> None:
        raise NotImplementedError


class SampleGFKObjectMixIn:

    def setUp(self) -> None:
        super().setUp()

        counter = 1
        for ct in ContentType.objects.all():
            setattr(self, 'gfk_sample_object'+str(counter), ct)
            counter += 1
