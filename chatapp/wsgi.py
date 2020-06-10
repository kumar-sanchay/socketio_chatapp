"""
WSGI config for chatapp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
import eventlet
import eventlet.wsgi
from django.core.wsgi import get_wsgi_application
from socketio_app.views import sio
import socketio
from django.contrib.staticfiles.handlers import StaticFilesHandler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatapp.settings')

django_app = StaticFilesHandler(get_wsgi_application())
application = socketio.Middleware(sio, wsgi_app=django_app, socketio_path='socket.io')


eventlet.wsgi.server(eventlet.listen(('', 8000)), application)
