from django.db.models.signals import pre_save

from ..models import ChartItemData


def pre_save_chart_item_data(sender, instance, *args, **kwargs):
    instance.set_rank()


pre_save.connect(pre_save_chart_item_data, sender=ChartItemData)
