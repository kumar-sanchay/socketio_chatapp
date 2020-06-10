from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
import os
from django.http import HttpResponse
import socketio
from django.template.loader import render_to_string

async_mode = None

basedir = os.path.dirname(os.path.realpath(__file__))
sio = socketio.Server(async_mode=async_mode)
thread = None


def index(request):
    global thread
    if thread is None:
        thread = sio.start_background_task(background_thread)
    # user = get_object_or_404(User, pk=pk, username=username)
    # lst = [user.username, request.user.username]
    # print(lst)
    # lst.sort()
    # connector_username = lst[0]
    # rendered = render_to_string(str(os.path.join(basedir, 'templates/index.html')),
    #                             {'connector_username': str(connector_username)})
    return True


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        sio.sleep(10)
        count += 1
        sio.emit('my_response', {'data': 'Server generated event'},
                 namespace='/test')


@sio.event
def my_event(sid, message):
    sio.emit('my_response', {'data': message['data']}, room=sid)


@sio.event
def my_broadcast_event(sid, message):
    sio.emit('my_response', {'data': message['data']})


@sio.event
def join(sid, message):
    sio.enter_room(sid, message['room'])
    sio.emit('my_response', {'data': 'Connected: ' + message['room']},
             room=sid)


@sio.event
def leave(sid, message):
    sio.leave_room(sid, message['room'])
    sio.emit('my_response', {'data': 'Disconnected: ' + message['room']},
             room=sid)


@sio.event
def close_room(sid, message):
    sio.emit('my_response',
             {'data': 'Room ' + message['room'] + ' is closing.'},
             room=message['room'])
    sio.close_room(message['room'])


@sio.event
def my_room_event(sid, message):
    sio.emit('my_response', {'data': message['data'], 'sender': message['sender']},
             room=message['room'])


@sio.event
def disconnect_request(sid):
    sio.disconnect(sid)


@sio.event
def connect(sid, environ):
    sio.emit('my_response', {'data': 'Connected', 'count': 0}, room=sid)


@sio.event
def disconnect(sid):
    print('Client disconnected')


class Dashboard(LoginRequiredMixin, View):

    def get(self, request):
        users = User.objects.all()
        return render(request, 'dashboard.html', {'users': users})


class Chat(LoginRequiredMixin, View):

    def get(self, request, pk, username):
        user = get_object_or_404(User, pk=pk, username=username)
        lst = [user.username, request.user.username]
        print(lst)
        lst.sort()
        connector_username = lst[0]
        chat = index(request)
        if chat:
            return render(request, 'index.html', {'user': user, 'connector_username': connector_username})
        else:
            return HttpResponse('Failed')