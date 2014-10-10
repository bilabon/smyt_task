from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    (r'^$', TemplateView.as_view(template_name="main.html")),
    # API data v1
    url(r'^api/v1/users/$', 'data.views.list_users',
        name='api_list_users'),
    url(r'^api/v1/users/(?P<pk>\d+)/$', 'data.views.edit_user',
        name='api_edit_user'),
    url(r'^api/v1/users/fields/$', 'data.views.user_fields',
        name='api_user_fields'),

    url(r'^api/v1/rooms/$', 'data.views.list_rooms',
        name='api_list_rooms'),
    url(r'^api/v1/rooms/(?P<pk>\d+)/$', 'data.views.edit_room',
        name='api_edit_room'),
    url(r'^api/v1/rooms/fields/$', 'data.views.room_fields',
        name='api_room_fields'),
)
