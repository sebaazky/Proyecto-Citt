from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),      # root → core.urls
    ##path('administrador/', include('administrador.urls')),
    ##ppath('alumno/', include('alumno.urls')),
    ##ppath('capitan/', include('capitan.urls')),
    ##ppath('docente/', include('docente.urls')),
    ##ppath('login/', include('login.urls')),
    # ... otras apps ...
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
