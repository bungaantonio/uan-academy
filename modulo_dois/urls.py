from django.contrib import admin
from django.urls import path, include

from lancamento_pautas.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),

    path('accounts/', include('accounts.urls')),
    path('', home, name='home'),
    path('', include('lancamento_pautas.urls')),

]
