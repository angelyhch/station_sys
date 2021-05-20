from django.db.models.signals import pre_delete
from django.dispatch import receiver
from daily_focus.models import FocusImage, FocusAfterImage
from craft.utils import logger


@receiver(pre_delete, sender=FocusImage)
def image_delete(instance, **kwargs):
    logger.info('pre delete.')
    instance.image.delete(False)


@receiver(pre_delete, sender=FocusAfterImage)
def after_image_delete(instance, **kwargs):
    logger.info('pre delete.')
    instance.image.delete(False)

