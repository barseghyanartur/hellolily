from django.conf.urls import patterns, url

from lily.utils.views import ajax_update_view, notifications_view


urlpatterns = patterns('',
   url(r'^ajax/(?P<app_name>[A-Za-z]+)/(?P<model_name>[A-Za-z]+)/(?P<object_id>[0-9]+)/$', ajax_update_view, name='ajax_update_view'),
   url(r'^utils/notifications.js$', notifications_view, name='notifications'),
)
