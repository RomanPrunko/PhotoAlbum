from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    # Вбудовані URL для авторизації: login, logout, password_reset тощо
    path('accounts/', include('django.contrib.auth.urls')),
    path('albums/', include('albums.urls')),
    # Головна сторінка
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
]
