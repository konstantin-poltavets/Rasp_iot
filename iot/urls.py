from django.conf import settings
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('iot/modules-edit/<int:pk>/', views.modules_edit, name='modules_edit'),
    path('iot/modules-add/', views.modules_add, name='modules_add'),
    path('iot/list/', views.modules_list, name='modules_list'),
    path('iot/list-view/', views.ModulesListView.as_view(), name='modules_list_view'),
    path('iot/edit-view/<int:pk>/', views.ModulesDetailView.as_view(), name='modules_edit_view'),
    path('iot/boards-list/', views.BoardsListView.as_view(), name='boards_list'),
    path('iot/boards_edit/<int:pk>/', views.boards_edit, name='boards_edit'),
    path('iot/boards-add/', views.boards_add, name='boards_add'),
    path('iot/publish/', views.publish, name='publish'),
    path('iot/linkedboards/', views.linkedboards, name='linkedboards'),
    path('iot/mqttypes/', views.MqttypesListView.as_view(), name='mqttypes'),
    path('iot/mqtt/', views.MqttListView.as_view(), name='mqtt'),
    path('iot/publish/', views.publish, name='publish'),

]

