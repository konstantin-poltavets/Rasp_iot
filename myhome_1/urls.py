from django.urls import path
from myhome_1 import views

urlpatterns = [
    path('mqtt/', views.mqttViewSet.as_view({'get': 'list'}), name = 'logout_1'),
    path('gazjson/', views.GazListjson.as_view()),
    path('mqtt/<int:pk>/', views.mqttDetail.as_view()),
    path('graph/', views.graph_1, name = 'graph_1'),
    path('select/', views.select, name = 'select'),
    path('search/', views.search, name = 'search'),
    path('search_result/', views.search_result, name = 'search_result'),
    path('publish/', views.publish, name = 'publish'),
    path('publish_1/', views.publish_1, name = 'publish_1'),
    path('template/', views.view_func, name = 'template'),
    path('google_graphs/', views.publish_1, name = 'google_graphs'),
    path('google_rest_int/', views.google_rest_int, name = 'google_rest_int'),
    path('google_rest/', views.google_rest, name = 'google_rest'),
    path('gaz_list/', views.gazListView.as_view(), name='gaz_list'),
    path('gaz_detail/<int:pk>/', views.gazDetailView.as_view(), name='gaz_detail'),
    path('gaz_add/', views.gaz_add, name='gaz_add'),
    path('gaz_template/', views.gaz_template, name='gaz_template'),
    path('gaz_template_month/', views.gaz_template_month, name='gaz_template_month'),
    path('gaz_edit/<int:pk>/', views.gazoline_edit, name='gazoline_edit_view'),
    path('gaz_edit/<int:pk>/delete/', views.GazDelete.as_view(), name='gaz_del'),
    path('gaz_search/', views.gaz_search, name = 'gaz_search'),
    path('gaz_search_result/', views.gaz_search_result, name = 'gaz_search_result'),
    path('export/csv/', views.export_users_csv, name='export_users_csv'),
    path('back', views.get_success_url, name='get_success_url'),
    path('gchart', views.gchart, name='gchart_url'),
    path('get_stock/', views.get_stock, name="get_stock"),
]

