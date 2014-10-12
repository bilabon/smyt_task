# -*- coding: utf-8 -*-
from django.test import TestCase

from .models import Setting, default


class SettingModelTest(TestCase):

    def test_create(self):
        """
        Tests get/create Setting.
        """
        Setting.objects.create(title=default)
        obj_setting = Setting.objects.get(title=default)
        self.assertEqual(default, obj_setting.title)
