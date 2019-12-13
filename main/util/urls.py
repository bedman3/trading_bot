from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.views import debug

from main.views.api.server_status.health import ServerHealth, SecretHealth
from main.views.swagger import swagger_view


def get_url_patterns() -> list:
    urlpatterns = [
        path('', debug.default_urlconf),
        path('admin/', admin.site.urls),
        path('accounts/login/', LoginView.as_view(
            template_name='admin/login.html',
            extra_context={
                'site_header': 'User Login',
            }
        )),
        path('accounts/logout/', LogoutView.as_view()),
        path('api/swagger/', swagger_view.with_ui('swagger', cache_timeout=0)),
        path('api/redoc/', swagger_view.with_ui('redoc', cache_timeout=0))
    ]

    class_view_list = [
        ServerHealth,
        SecretHealth
    ]

    for class_view in class_view_list:
        urlpatterns.append(path(class_view.url, class_view.as_view()))

    return urlpatterns
