from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import Cliente, MensagemContato, Produto, Parceiro # Importe Parceiro
from .forms import CustomUserCreationForm, ProdutoForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Max

def home(request):
    """
    Renderiza a página inicial (landing page) com o carrossel de parceiros.
    """
    # Busca todos os parceiros para o carrossel
    parceiros = Parceiro.objects.all().order_by('nome_loja')
    
    context = {
        'parceiros': parceiros
    }
    return render(request, 'home.html', context)

def sobre(request):
    """
    Renderiza a página "Sobre".
    """
    return render(request, 'sobre.html')

def contato(request):
    """
    Renderiza a página "Contato" e processa o envio de mensagens.
    """
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        mensagem_texto = request.POST.get('mensagem')

        if nome and email and mensagem_texto:
            # Validação básica de e-mail (além do tipo de campo no HTML)
            if "@" not in email or "." not in email:
                messages.error(request, "Por favor, insira um endereço de e-mail válido.")
            else:
                # Cria e salva a nova mensagem no banco de dados
                MensagemContato.objects.create(
                    nome=nome,
                    email=email,
                    mensagem=mensagem_texto
                )
                messages.success(request, "Sua mensagem foi enviada com sucesso! Em breve entraremos em contato.")
                return redirect('contato') # Redireciona para evitar reenvio do formulário
        else:
            messages.error(request, "Por favor, preencha todos os campos do formulário.")
    return render(request, 'contato.html')

def cadastro(request):
    """
    Renderiza a página de "Cadastro" e processa o registro de novos clientes.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST) # Usa o CustomUserCreationForm
        if form.is_valid():
            user = form.save() # Salva o novo usuário (User) no banco de dados, incluindo o email

            # Agora, crie o perfil Cliente e vincule-o ao usuário recém-criado
            nome_completo = request.POST.get('nome_completo')
            telefone = request.POST.get('telefone')

            cliente = Cliente.objects.create(
                user=user,
                nome_completo=nome_completo,
                telefone=telefone
            )
            messages.success(request, 'Cadastro realizado com sucesso! Faça login para continuar.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Erro no campo '{field}': {error}")
            # Se a senha não for válida, CustomUserCreationForm já trata as mensagens de erro
    else:
        form = CustomUserCreationForm() # Cria um formulário vazio do seu CustomUserCreationForm
    return render(request, 'cadastro.html', {'form': form})


def login_view(request):
    """
    Renderiza a página de "Login" e processa a autenticação de clientes.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user) # Faz o login do usuário
                messages.success(request, f"Bem-vindo(a) de volta, {user.username}!")
                return redirect('home') # Redireciona para a home ou dashboard do usuário
            else:
                messages.error(request, "Nome de usuário ou senha inválidos.")
        else:
            messages.error(request, "Nome de usuário ou senha inválidos.")
    else:
        form = AuthenticationForm() # Cria um formulário vazio para exibir
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    """
    Realiza o logout do usuário.
    """
    logout(request)
    messages.info(request, "Você foi desconectado(a).")
    return redirect('home') # Redireciona para a página inicial

# Função auxiliar para verificar se o usuário é staff (admin)
def is_staff(user):
    return user.is_authenticated and user.is_staff

@login_required(login_url='login') # Garante que o usuário esteja logado
@user_passes_test(is_staff, login_url='home') # Garante que o usuário seja staff
def cadastrar_produto(request):
    """
    Permite que usuários admin cadastrem novos produtos.
    """
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES) # request.FILES para lidar com o upload de fotos
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto cadastrado com sucesso!')
            return redirect('cadastrar_produto') # Redireciona para a mesma página ou para uma lista de produtos
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Erro no campo '{field}': {error}")
            if form.non_field_errors(): # Erros que não estão ligados a um campo específico
                for error in form.non_field_errors():
                    messages.error(request, f"Erro: {error}")
    else:
        form = ProdutoForm() # Formulário vazio para GET request
    return render(request, 'cadastro_produto.html', {'form': form})

def lista_parceiros(request):
    """
    Exibe uma lista de todos os parceiros disponíveis.
    """
    # Busca todos os parceiros ordenados pelo nome da loja
    parceiros = Parceiro.objects.all().order_by('nome_loja')
    context = {
        'parceiros': parceiros
    }
    return render(request, 'parceiros.html', context)


# VIEW ATUALIZADA: Lista de Produtos com Lançamento em Destaque
def lista_produtos(request):
    # Encontra o produto com o maior valor, se houver
    produto_lancamento = None
    todos_produtos = Produto.objects.filter(disponivel=True)

    if todos_produtos.exists():
        # Encontra o valor máximo
        maior_valor = todos_produtos.aggregate(Max('valor'))['valor__max']
        
        # Encontra o produto com o maior valor (se houver mais de um com o mesmo valor, pega o primeiro)
        produto_lancamento = todos_produtos.filter(valor=maior_valor).order_by('-data_cadastro').first() # Se mais de um, pega o mais recente

        # Filtra os demais produtos, excluindo o produto de lançamento
        outros_produtos = todos_produtos.exclude(pk=produto_lancamento.pk).order_by('nome')
    else:
        outros_produtos = Produto.objects.none() # Retorna um QuerySet vazio se não houver produtos

    context = {
        'produto_lancamento': produto_lancamento,
        'outros_produtos': outros_produtos,
    }
    return render(request, 'produtos.html', context)

# Detalhe do Produto
def detalhe_produto(request, produto_id):
    """
    Exibe os detalhes de um produto específico.
    """
    # Busca um produto pelo ID. Se não encontrar, retorna um erro 404.
    produto = get_object_or_404(Produto, pk=produto_id)
    context = {
        'produto': produto
    }
    return render(request, 'detalhe_produto.html', context)