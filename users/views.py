from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth import views as auth_views
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import PasswordRecoveryForm
from cart.models import Cart  # 👈 Importe o modelo Cart
from produtos.models import Produto  # 👈 Importe o modelo Produto

# ========== LOGOUT ==========
def logout_view(request):
    """Faz o logout do usuário"""
    logout(request)
    return HttpResponseRedirect(reverse('index'))

# ========== LOGIN PERSONALIZADO ==========
class CustomLoginView(auth_views.LoginView):
    """View de login personalizada que processa produto pendente"""
    template_name = 'users/login.html'
    
    def form_valid(self, form):
        """Processa o login e verifica se há produto pendente"""
        # Primeiro, faz o login normal
        response = super().form_valid(form)
        
        # Verifica se há um produto pendente na sessão
        pending_product = self.request.session.get('pending_product')
        if pending_product:
            # Limpa da sessão
            del self.request.session['pending_product']
            
            # Adiciona o produto ao carrinho automaticamente
            try:
                # Obtém ou cria o carrinho do usuário
                cart_obj, _ = Cart.objects.new_or_get(self.request)
                
                # Busca o produto
                product = Produto.objects.get(id=pending_product['id'])
                
                # Adiciona ao carrinho
                if pending_product['action'] == 'add':
                    cart_obj.add_product(product, pending_product['quantity'])
                    
                # Mensagem de sucesso
                messages.success(self.request, f'✅ {product.nome} adicionado ao carrinho!')
                
                # Redireciona para o carrinho
                return redirect('carts:home')
            except Produto.DoesNotExist:
                messages.error(self.request, '❌ Produto não encontrado.')
            except Exception as e:
                messages.error(self.request, f'Erro ao adicionar produto: {str(e)}')
        
        return response

# ========== REGISTRO ==========
def register(request):
    """Faz o cadastro de um novo usuário"""
    if request.method != 'POST':
        # Exibe o formulário de cadastro em branco
        form = UserCreationForm()
    
    else:
        # Processa o formulário preenchido
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # Faz o login do usuário e o redireciona para a página inicial
            authenticated_user = authenticate(username=new_user.username, password=request.POST['password1'])
            login(request, authenticated_user)

            # Verifica se há produto pendente APÓS o registro
            pending_product = request.session.get('pending_product')
            if pending_product:
                try:
                    cart_obj, _ = Cart.objects.new_or_get(request)
                    product = Produto.objects.get(id=pending_product['id'])
                    cart_obj.add_product(product, pending_product['quantity'])
                    messages.success(request, f'✅ {product.nome} adicionado ao carrinho!')
                    del request.session['pending_product']
                    return redirect('carts:home')
                except:
                    pass

            return HttpResponseRedirect(reverse('index'))
    
    context = {'form': form}
    return render(request, 'users/register.html', context)

# ========== RECUPERAR SENHA ==========
def recover(request):
    """Recupera/altera a senha do usuário"""
    if request.method != 'POST':
        # Exibe o formulário de recuperação em branco
        form = PasswordRecoveryForm()
    else:
        # Processa o formulário preenchido
        form = PasswordRecoveryForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            new_password = form.cleaned_data['new_password']
            
            # Busca o usuário e altera a senha
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            
            # (Opcional) Faz login automático após alterar a senha
            authenticated_user = authenticate(username=username, password=new_password)
            if authenticated_user is not None:
                login(request, authenticated_user)
                
                # Verifica se há produto pendente
                pending_product = request.session.get('pending_product')
                if pending_product:
                    try:
                        cart_obj, _ = Cart.objects.new_or_get(request)
                        product = Produto.objects.get(id=pending_product['id'])
                        cart_obj.add_product(product, pending_product['quantity'])
                        messages.success(request, f'✅ {product.nome} adicionado ao carrinho!')
                        del request.session['pending_product']
                        return redirect('carts:home')
                    except:
                        pass
            
            # Redireciona para a página inicial com mensagem de sucesso
            messages.success(request, '✅ Senha alterada com sucesso!')
            return HttpResponseRedirect(reverse('index'))
    
    context = {'form': form}
    return render(request, 'users/recover.html', context)