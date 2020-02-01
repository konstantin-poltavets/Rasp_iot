from django.urls import path
from myhome_1 import views

urlpatterns = [
    path('mqtt/', views.mqttViewSet.as_view({'get': 'list'}), name = 'logout_1'),
    path('mqtt/<int:pk>/', views.mqttDetail.as_view()),
    path('graph/', views.graph_1, name = 'graph_1'),
    path('select/', views.select, name = 'select'),
    path('search/', views.search, name = 'search'),
    path('search_result/', views.search_result, name = 'search_result'),
    path('publish/', views.publish, name = 'publish'),
    path('publish_1/', views.publish_1, name = 'publish_1'),
    path('template/', views.view_func, name = 'template'), # TODO
    path('google_graphs/', views.publish_1, name = 'google_graphs'),
    path('google_rest_int/', views.google_rest_int, name = 'google_rest_int'),
    path('google_rest/', views.google_rest, name = 'google_rest'),
    path('gaz_list/', views.gazListView.as_view(), name='gaz_list'),

]

