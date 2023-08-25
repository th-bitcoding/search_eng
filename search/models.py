
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.
class Search(models.Model):
    search_data = models.JSONField()

@receiver(post_save, sender=Search)
def search_post_save(sender, instance, **kwargs):
    json_data = instance.search_data
    try:
        sub_obj = json_data['TV_Data']['Channel_List']['main']['sub']
    except:
        pass
    for obj in sub_obj:
        SubObjectJSON.objects.update_or_create(
            sub_objects = sub_obj[obj]
        )


class SubObjectJSON(models.Model):
    sub_objects = models.JSONField()