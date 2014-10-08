#from django.shortcuts import render
import json
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from annoying.decorators import ajax_request
from .forms import UserForm
from .models import User


@ajax_request
@csrf_exempt
def list_users(request):
    """List of all users api requests.
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
        return {'success': False, 'message': 'Not valid request'}


@ajax_request
@csrf_exempt
def edit_user(request, pk):
    """Edit User by given ID"""

    print 'edit_user pk=', pk
    if request.method == 'POST':
        form = UserForm(request.POST)
        form.is_valid()
        user = User.objects.filter(id=pk)
        if user.exists():
            user.update(**form.cleaned_data)
            user = serializers.serialize('json', user)
        else:
            return {'success': False, 'message': 'Wrong ID'}
        return {'success': True}
    else:
        return {'success': False, 'message': 'Not valid request!'}
