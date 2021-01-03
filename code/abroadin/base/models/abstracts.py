from django.contrib.contenttypes.models import ContentType
from django.db import models, transaction


class InheritanceCastModel(models.Model):
    """
    An abstract base class that provides a ``real_type`` FK to ContentType.

    For use in trees of inherited models, to be able to downcast
    parent instances to their child types.

    """
    real_type = models.ForeignKey(ContentType, null=True, on_delete=models.PROTECT, editable=False)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.real_type = self._get_real_type()
        super().save(*args, **kwargs)

    def _get_real_type(self):
        return ContentType.objects.get_for_model(type(self))

    def cast(self):
        return self.real_type.get_object_for_this_type(pk=self.pk)

    class Meta:
        abstract = True
