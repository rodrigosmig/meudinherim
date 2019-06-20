"""
WSGI config for meudinherim project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""
import os, secrets

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meudinherim.settings")
os.environ['SENDGRID_API_KEY'] = secrets.SENDGRID_API_KEY

application = get_wsgi_application()
