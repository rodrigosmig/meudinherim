from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UsuarioProfile(models.Model):

	user = models.OneToOneField(User)
	email = models.EmailField()

	def __str__(self):

		return self.user.username