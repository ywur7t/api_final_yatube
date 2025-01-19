from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse


def redirect_to_redoc(request):
    redoc_url = request.build_absolute_uri(reverse('redoc'))
    return HttpResponseRedirect(redoc_url)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path('', redirect_to_redoc),
]
