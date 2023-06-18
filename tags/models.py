from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from store.models import Product


class TaggedItemManager(models.Manager):
    def get_tags_for(self, obj_type, obj_id):
        contnet_type = ContentType.objects.get_for_model(obj_type)

        return TaggedItem.objects.filter(
            contnet_type=contnet_type, 
            object_id=obj_id
        )


class Tag(models.Model):
    label = models.CharField(max_length=255)


class TaggedItem(models.Model):
    objects = TaggedItemManager()
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
