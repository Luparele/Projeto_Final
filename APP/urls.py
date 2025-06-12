from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sobre/', views.sobre, name='sobre'),
    path('contato/', views.contato, name='contato'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('produtos/cadastrar/', views.cadastrar_produto, name='cadastrar_produto'),
    path('produtos/', views.lista_produtos, name='lista_produtos'),
    path('produtos/<int:produto_id>/', views.detalhe_produto, name='detalhe_produto'),
    path('parceiros/', views.lista_parceiros, name='lista_parceiros'), # NOVA URL
]