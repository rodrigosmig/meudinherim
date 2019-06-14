from django.db import models
from django.contrib.auth.models import User

class UsuarioProfile(models.Model):

	user = models.OneToOneField(User)
	foto = models.ImageField(upload_to = 'foto_perfil/', blank = True)
	mail_contas_a_pagar = models.BooleanField(default = False)

	def __str__(self):

		return self.user.username