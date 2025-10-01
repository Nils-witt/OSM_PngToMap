from django.db import models
from django.conf import settings
import uuid
# Create your models here.


class UUIDMixIn(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TimeStampMixIn(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class OwnerShipMixIn(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, null=True)

    class Meta:
        abstract = True


class Project(UUIDMixIn, TimeStampMixIn, OwnerShipMixIn):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='project_images/', blank=True, null=True)

    min_zoom = models.IntegerField(default=10)
    max_zoom = models.IntegerField(default=16)
    coordinates = models.JSONField(blank=True, null=True)  # Expecting a list of [lat, lon] pairs

    status = models.CharField(max_length=50, default='draft',choices=[('draft', 'Draft'),('pending', 'Pending'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('failed', 'Failed')])

    def __str__(self):
        return self.name