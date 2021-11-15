import uuid

from django.db import models

from commons.models import BaseClass

class Article(BaseClass):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	author = models.ForeignKey('authors.Author', related_name='articles', on_delete=models.CASCADE)
	category = models.CharField(max_length=80)
	title = models.CharField(max_length=200)
	summary = models.TextField()
	first_paragraph = models.TextField()
	body = models.TextField()

	def __str__(self):
		return self.name