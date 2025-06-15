"""
URL configuration for JWC project.
"""
from django.contrib import admin
from django.urls import path, include
# Importações para servir arquivos de mídia (Comentar ou remover estas linhas)
# from django.conf import settings
# from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('APP.urls')), # Inclui as URLs do seu app APP
]

# Configuração para servir arquivos de mídia apenas em ambiente de desenvolvimento (Comentar ou remover todo este bloco)
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)