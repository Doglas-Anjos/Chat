from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView # new
from .views import *
urlpatterns = [
    path('chat/', include('chat.urls')),
    path('admin/', admin.site.urls),
    path('', LogarUsuario.as_view(), name="logar_usuario"),
    path('cadastrar_usuario/', cadastrar_usuario, name="cadastrar_usuario"),
    path('deslogar_usuario/', deslogar_usuario, name="deslogar_usuario"),
    path('alterar_senha/', alterar_senha, name='alterar_senha'),
]
