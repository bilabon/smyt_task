# -*- coding: utf-8 -*-
import json
from django_webtest import WebTest
from django.core.urlresolvers import reverse

from .models import User, Room


class UserTest(WebTest):

    def test_model_create(self):
        """
        Tests get/create User.
        """
        User.objects.create(name='John',
                            paycheck=12,
                            date_joined='2012-12-12')
        obj_user = User.objects.get(name='John')
        self.assertEqual('John', obj_user.name)
        self.assertEqual(12, obj_user.paycheck)

    def test_api_get_users(self):
        """
        Test API: get all users
        """
        User.objects.create(name='John Smit',
                            paycheck=12,
                            date_joined='2012-12-12')
        resp = self.app.get(reverse('api_users'))
        data = json.loads(resp.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['users'][0]['fields']['name'], 'John Smit')

    def test_api_create_user(self):
        """
        Test API: create user
        """
        data = {}
        data['name'] = 'Joe Bloggs'
        data['paycheck'] = 12
        data['date_joined'] = '2012-10-12'
        resp = self.app.post(reverse('api_users'), data)
        data = json.loads(resp.content)
        self.assertTrue(data['success'])
        self.assertTrue(User.objects.get(name='Joe Bloggs'))

    def test_api_update_user(self):
        """
        Test API: update user
        """
        User.objects.create(name='John G.',
                            paycheck=12,
                            date_joined='2012-12-12')
        user = User.objects.get(name='John G.')
        data = {}
        data['name'] = 'John D.'
        data['paycheck'] = user.paycheck
        data['date_joined'] = user.date_joined
        resp = self.app.post(
            reverse('api_edit_user', kwargs={'pk': user.pk}), data)
        data = json.loads(resp.content)
        self.assertTrue(data['success'])

    def test_api_fields_user(self):
        """
        Test API: show all User model fields
        """
        resp = self.app.get(reverse('api_user_fields'))
        data = json.loads(resp.content)
        fields = User._meta.get_all_field_names()
        if 'id' in fields:
            fields.remove('id')
        self.assertEqual(data, fields)


class RoomTest(WebTest):

    def test_model_create(self):
        """
        Tests get/create Room.
        """
        Room.objects.create(department='#1', spots=11)
        obj_room = Room.objects.get(department='#1')
        self.assertEqual('#1', obj_room.department)
        self.assertEqual(11, obj_room.spots)

    def test_api_get_rooms(self):
        """
        Test API: get all rooms
        """
        Room.objects.create(department='#2', spots=12)
        resp = self.app.get(reverse('api_rooms'))
        data = json.loads(resp.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['rooms'][0]['fields']['department'], '#2')

    def test_api_create_room(self):
        """
        Test API: create room
        """
        data = {}
        data['department'] = '#3'
        data['spots'] = 13
        resp = self.app.post(reverse('api_rooms'), data)
        data = json.loads(resp.content)
        self.assertTrue(data['success'])
        self.assertTrue(Room.objects.get(department='#3'))

    def test_api_update_room(self):
        """
        Test API: update room
        """
        room = Room.objects.create(department='#4', spots=14)
        data = {}
        data['department'] = '#444'
        data['spots'] = 1444
        resp = self.app.post(
            reverse('api_edit_room', kwargs={'pk': room.pk}), data)
        data = json.loads(resp.content)
        self.assertTrue(data['success'])

    def test_api_fields_room(self):
        """
        Test API: show all room model fields
        """
        resp = self.app.get(reverse('api_room_fields'))
        data = json.loads(resp.content)
        fields = Room._meta.get_all_field_names()
        if 'id' in fields:
            fields.remove('id')
        self.assertEqual(data, fields)
