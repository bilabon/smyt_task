import json
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from annoying.decorators import ajax_request
from .forms import UserForm, RoomForm
from .models import User, Room


not_valid_request = {'success': False, 'message': 'Not valid request'}


@ajax_request
@csrf_exempt
def list_users(request):
    """API for Users.
    If request.GET: return all Users
    If request.POST: Create User
    """
    print 'list_users'
    if request.method == 'GET':
        users = serializers.serialize('json', User.objects.all())
        return {'success': True, 'users': json.loads(users)}

    elif request.method == 'POST':

        form = UserForm(request.POST)
        if not form.is_valid():
            return {'success': False, 'message': form.errors}

        user = User.objects.create(**form.cleaned_data)
        user = serializers.serialize('json', [user])
        return {'success': True, 'user': json.loads(user)}
    else:
        return not_valid_request


@ajax_request
@csrf_exempt
def edit_user(request, pk):
    """Edit User by given ID"""
    print 'edit_user pk=', pk
    if request.method == 'POST':
        user = User.objects.filter(id=pk)
        if user.exists():
            form = UserForm(request.POST)
            form.is_valid()
            data = form.cleaned_data
            data = {key: value for key, value in data.items() if value}
            user.update(**data)
        else:
            return {'success': False, 'message': 'Wrong ID'}
        return {'success': True}
    else:
        return not_valid_request


@ajax_request
def user_fields(request):
    """Return all field names of model User"""
    if request.method == 'GET':
        fields = User._meta.get_all_field_names()
        if 'id' in fields:
            fields.remove('id')
        return fields
    else:
        return not_valid_request


@ajax_request
@csrf_exempt
def list_rooms(request):
    """API for Rooms.
    If request.GET: return all Room
    If request.POST: Create Room
    """
    print 'list_users'
    if request.method == 'GET':
        rooms = serializers.serialize('json', Room.objects.all())
        return {'success': True, 'rooms': json.loads(rooms)}

    elif request.method == 'POST':

        form = RoomForm(request.POST)
        if not form.is_valid():
            return {'success': False, 'message': form.errors}

        room = Room.objects.create(**form.cleaned_data)
        room = serializers.serialize('json', [room])
        return {'success': True, 'rooms': json.loads(room)}
    else:
        return not_valid_request


@ajax_request
@csrf_exempt
def edit_room(request, pk):
    """Edit Room by given ID"""
    print 'edit_user pk=', pk
    if request.method == 'POST':
        room = Room.objects.filter(id=pk)
        if room.exists():
            form = RoomForm(request.POST)
            form.is_valid()
            data = form.cleaned_data
            data = {key: value for key, value in data.items() if value}
            room.update(**data)
        else:
            return {'success': False, 'message': 'Wrong ID'}
        return {'success': True}
    else:
        return not_valid_request


@ajax_request
def room_fields(request):
    """Return all field names of model Room"""
    if request.method == 'GET':
        fields = Room._meta.get_all_field_names()
        if 'id' in fields:
            fields.remove('id')
        return fields
    else:
        return not_valid_request
