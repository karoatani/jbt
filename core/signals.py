from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Tracking, Job


@receiver(post_save, sender=Job)
def create_tracking(sender, instance, created, **kwargs):
    if created:
        tracking = Tracking.objects.create(job=instance)
        tracking.save()
