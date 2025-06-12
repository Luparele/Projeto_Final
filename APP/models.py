from django.db import models
from django.contrib.auth.models import User

# Modelo para perfis de clientes
class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.nome_completo

# Modelo para mensagens de contato
class MensagemContato(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    mensagem = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Mensagem de Contato"
        verbose_name_plural = "Mensagens de Contato"
        ordering = ['-data_envio']

    def __str__(self):
        return f"Mensagem de {self.nome} ({self.email}) em {self.data_envio.strftime('%d/%m/%Y %H:%M')}"

# Modelo: Produto (Androide Humanoide)
class Produto(models.Model):
    nome = models.CharField(max_length=200, unique=True) # Nome único para cada produto
    foto = models.ImageField(upload_to='produtos_fotos/') # Onde as imagens serão salvas
    historia = models.TextField(blank=True, null=True) # História/descrição detalhada
    aplicacao = models.TextField(blank=True, null=True) # Exemplos de aplicação/uso
    valor = models.DecimalField(max_digits=10, decimal_places=2) # Preço do produto
    disponivel = models.BooleanField(default=True) # Se o produto está em estoque/disponível
    data_cadastro = models.DateTimeField(auto_now_add=True) # Data de cadastro

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['nome'] # Ordena os produtos pelo nome

    def __str__(self):
        return self.nome

# NOVO MODELO: Parceiro
class Parceiro(models.Model):
    nome_loja = models.CharField(max_length=200, unique=True)
    logo = models.ImageField(upload_to='parceiros_logos/', blank=True, null=True) # Logo da loja (opcional)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    site_url = models.URLField(max_length=200, blank=True, null=True) # Link para o site da loja
    data_cadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Parceiro"
        verbose_name_plural = "Parceiros"
        ordering = ['nome_loja']

    def __str__(self):
        return self.nome_loja