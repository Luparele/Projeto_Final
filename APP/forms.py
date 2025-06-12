from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Produto # Importa o novo modelo Produto

class CustomUserCreationForm(UserCreationForm):
    # Adicione o campo de e-mail como um campo de formulário
    email = forms.EmailField(label="E-mail", required=True)

    class Meta(UserCreationForm.Meta):
        # Campos do modelo User que este formulário vai usar
        # Adicione 'email' à lista de campos
        model = User
        fields = UserCreationForm.Meta.fields + ('email',) # Adiciona 'email' aos campos existentes

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está em uso.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False) # Salva o usuário sem comitar no DB ainda
        user.email = self.cleaned_data['email'] # Atribui o email ao objeto User
        if commit:
            user.save() # Agora salva o User com o email
        return user

# NOVO FORMULÁRIO: Para o cadastro de produtos
class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        # Campos que queremos incluir no formulário
        fields = ['nome', 'foto', 'historia', 'aplicacao', 'valor', 'disponivel']
        # Opcional: Adicionar widgets para customizar a aparência dos campos
        widgets = {
            'historia': forms.Textarea(attrs={'rows': 5}),
            'aplicacao': forms.Textarea(attrs={'rows': 5}),
            'valor': forms.NumberInput(attrs={'step': '0.01'})
        }
        labels = { # Customiza os labels que aparecem no formulário
            'nome': 'Nome do Produto',
            'foto': 'Foto do Produto',
            'historia': 'História / Descrição Detalhada',
            'aplicacao': 'Aplicações e Usos',
            'valor': 'Valor (R$)',
            'disponivel': 'Disponível para Venda',
        }