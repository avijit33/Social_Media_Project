from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from postapp import views
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('loginapp.urls')),
    path('post/', include('postapp.urls')),
    path('', views.home, name = "home"),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
