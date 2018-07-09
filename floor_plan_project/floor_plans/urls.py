from django.conf.urls import url
from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from floor_plan_project.floor_plans import views

app_name = 'floor_plans'
urlpatterns = [
    re_path('^$', views.api_root),
    re_path('^image_records/$', views.ImageRecordList.as_view(), name='imagerecord-list'),
    re_path('^image_records/(?P<pk>[0-9]+)/$', views.ImageRecordDetail.as_view(), name='imagerecord-detail'),
    re_path('^classifications/$', views.ClassificationList.as_view(), name='classification-list'),
    re_path('^classifications/(?P<pk>[0-9]+)/$', views.ClassificationDetail.as_view(), name='classification-detail'),
    re_path('^classifiers/$', views.ClassifierList.as_view(), name='classifier-list'),
    re_path('^classifiers-types/$', views.ClassifierTypeList.as_view(), name='classifier-types-list'),
    re_path('^classifiers/(?P<pk>[0-9]+)/$', views.ClassifierDetail.as_view(), name='classifier-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
