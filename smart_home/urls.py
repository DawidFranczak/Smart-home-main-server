import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("log.urls")),
    path("rpl/", include("rpl.urls")),
    path("wykres/", include("chart.urls")),
    path("swiatla/", include("light.urls")),
    path("schody/", include("stairs.urls")),
    path("rolety/", include("sunblind.urls")),
    path("akwaria/", include("aquarium.urls")),
    path("urzadzenia/", include("devices.urls")),
    path("ustawienia/", include("user_page.urls")),
    path("api/rpl/", include("rpl.api.urls")),
    path("api/check/", include("rpl.api.urls")),
    path("api/chart/", include("chart.api.urls")),
    path("api/stairs/", include("stairs.api.urls")),
    path("api/aquarium/", include("aquarium.api.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "log.views.handling_404"
