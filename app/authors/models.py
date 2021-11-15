import uuid

from django.db import models

from commons.models import BaseClass

class Author(BaseClass):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	name = models.CharField(max_length=100)
	picture = models.ImageField(upload_to='authors/pictures/', null=True, blank=True)

	def __str__(self):
		return self.name