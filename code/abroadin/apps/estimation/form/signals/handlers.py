from django.db.models.signals import pre_save, pre_delete, post_save, post_delete, m2m_changed

from abroadin.apps.estimation.form.models import StudentDetailedInfo
from abroadin.apps.estimation.form.tasks import update_student_detailed_info_ranks


def post_save_student_detailed_info(sender, instance, *args, **kwargs):
    # update_student_detailed_info_ranks()
    pass


post_save.connect(post_save_student_detailed_info, sender=StudentDetailedInfo)
