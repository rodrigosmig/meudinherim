from django.db import models
from django.contrib.auth.models import User

class ConfigModal(models.Model):

	nick = models.CharField(max_length = 20)
	senha = models.CharField(max_length= 30)
	email = models.CharField(max_length= 30)
	user = models.ForeignKey(User, on_delete = models.CASCADE)
