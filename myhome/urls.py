from django.contrib import admin
from django.urls import path, include
from django.conf.urls import *
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name = 'index'),
    path('logout/', views.logout_view, name = 'logout_1'),
    path('first/', views.first, name = 'first'),
    path('admin/', admin.site.urls),
    path('register/', views.RegisterFormView.as_view()),
    path('accounts/', include('django.contrib.auth.urls')), 
    path('api/', include('api.urls')),
    path('api-my/', include('rest_framework.urls', namespace = 'rest_framework')),
    path ('api-mqtt/', include('myhome_1.urls')),
    path('', include('iot.urls')),
    path('status/', views.pi_status, name = 'pi_status'),

]


if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()