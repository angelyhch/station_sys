from django.db.models.signals import pre_delete
from django.dispatch import receiver
from daily_focus.models import Focus, FocusImage, FocusAfterImage
from craft.utils import logger


@receiver(pre_delete, sender=Focus)
def Focus_delete(instance, **kwargs):
    logger.info(f'{instance.user.username} delete id[{instance.id}]')


@receiver(pre_delete, sender=FocusImage)
def image_delete(instance, **kwargs):
    logger.info(f'{instance.focus.user.username} delete id[{instance.id}]')
    instance.image.delete(False)


@receiver(pre_delete, sender=FocusAfterImage)
def after_image_delete(instance, **kwargs):
    logger.info(f'{instance.focus.user.username} delete id[{instance.id}]')
    instance.image.delete(False)

