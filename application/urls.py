from django.conf.urls import include, url
from . import views

urlpatterns = [
    #url(r'^$', views.Index.as_view(), name="index"),
    #url(r'^$', views.index_waiting, name="index"),
    url(r'^$', views.index_result, name="index"),
    url(r'^coming/$', views.coming, name="coming"),
    url(r'^upload/$', views.upload, name="file_upload"),
    url(r'^bring_chaperone/$', views.bring_chaperone, name="bring_chaperone"),
    url(r'^accounts/profile/$', views.profile_redirect, name="profile_redirect"),
    url(r'^csv/$', views.csv_export, name="csv_export"),
]