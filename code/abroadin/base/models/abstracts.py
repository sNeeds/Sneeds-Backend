from django.contrib.contenttypes.models import ContentType
from django.db import models, transaction


class InheritanceCastModel(models.Model):
    """
    An abstract base class that provides a ``real_type`` FK to ContentType.

    For use in trees of inherited models, to be able to downcast
    parent instances to their child types.

    """
    real_type = models.ForeignKey(ContentType, on_delete=models.PROTECT, editable=False)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.real_type = self._get_real_type(using=kwargs.get('using'))
        super().save(*args, **kwargs)

    def _get_real_type(self, *args, **kwargs):
        using = kwargs.pop('using', None)
        if using:
            ct = ContentType.objects.get_for_model(type(self))
            return ContentType.objects.using(using).get(app_label=ct.app_label, model=ct.model)
        return ContentType.objects.get_for_model(type(self))

    def cast(self):
        return self.real_type.get_object_for_this_type(pk=self.pk)

    class Meta:
        abstract = True
