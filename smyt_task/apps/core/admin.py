from django.contrib import admin
from smyt_task import settings
from .models import Setting


class SettingAdmin(admin.ModelAdmin):

    def has_add_permission(self, *args, **kwargs):
        return not Setting.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        with open(settings.root('apps') + '/core/model.yml', 'w') as s_file:
            s_file.write(obj.title)
        obj.save()

admin.site.register(Setting, SettingAdmin)
