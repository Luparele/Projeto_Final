from django.contrib import admin
from .models import Cliente, MensagemContato, Produto, Parceiro # Importe Parceiro

# Register your models here.
admin.site.register(Cliente)
admin.site.register(MensagemContato)
admin.site.register(Produto)
admin.site.register(Parceiro) # Registra o novo modelo Parceiro