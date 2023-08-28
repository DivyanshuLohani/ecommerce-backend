from django.db import models
import uuid
from shortuuidfield import ShortUUIDField


class BaseModel(models.Model):

    class Meta:
        abstract = True

    uid = ShortUUIDField(max_length=14, auto=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
