from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from produtos.models import Produto
from .models import Cart
from urllib.parse import quote


class CartHomeView(View):
    def get(self, request):
        cart_obj, _ = Cart.objects.new_or_get(request)
        return render(request, "cart/home.html", {"cart": cart_obj})


class CartUpdateView(View):
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        action     = request.POST.get('action', 'add')
        quantity   = int(request.POST.get('quantity', 1))
        tamanho    = request.POST.get('tamanho', '').strip() or None

        # Verifica login
        if not request.user.is_authenticated:
            request.session['pending_product'] = {
                'id':       product_id,
                'quantity': quantity,
                'action':   action,
                'tamanho':  tamanho,
            }
            messages.warning(request, 'Você precisa estar logado para adicionar produtos ao carrinho.')
            return redirect(f"{reverse('users:login')}?next={request.META.get('HTTP_REFERER', '')}")

        cart_obj, _ = Cart.objects.get_or_create_for_request(request)

        try:
            product = Produto.objects.get(id=product_id)
        except Produto.DoesNotExist:
            return redirect('carts:home')

        if action == 'add':
            # Validação backend: produto tem tamanhos mas nenhum foi selecionado
            if product.tem_tamanhos() and not tamanho:
                messages.error(request, 'Selecione um tamanho antes de adicionar ao carrinho.')
                referer = request.META.get('HTTP_REFERER', '')
                return redirect(referer or 'carts:home')

            cart_obj.add_product(product, quantity, tamanho=tamanho)

        elif action == 'delete':
            cart_obj.remove_product(product, 999, tamanho=tamanho)

        referer = request.META.get('HTTP_REFERER', '')
        if 'produto' in referer:
            return redirect('produto_detalhe', produto_id=product_id)

        return redirect('carts:home')


class CartClearView(LoginRequiredMixin, View):
    login_url = '/users/login/'
    redirect_field_name = 'next'

    def post(self, request, *args, **kwargs):
        cart_obj, _ = Cart.objects.new_or_get(request)
        cart_obj.clear_cart()
        return redirect('carts:home')


class CartWhatsAppView(LoginRequiredMixin, View):
    login_url = '/users/login/'
    redirect_field_name = 'next'

    def get(self, request):
        cart_obj, _ = Cart.objects.new_or_get(request)
        numero_whatsapp = getattr(settings, 'WHATSAPP_NUMBER', '5538999272628')
        mensagem = self._gerar_mensagem_pedido(cart_obj)
        whatsapp_link = f"https://wa.me/{numero_whatsapp}?text={quote(mensagem)}"
        return redirect(whatsapp_link)

    def _gerar_mensagem_pedido(self, cart):
        linhas = []
        linhas.append("🛍️ *NOVO PEDIDO - DeboraBy Joias*")
        linhas.append("")
        linhas.append("*ITENS:*")

        total = 0
        for item in cart.get_cart_items():
            preco    = float(item.product.preco)
            subtotal = float(item.get_total_price())
            total   += subtotal

            tam_info = f' — Tamanho: {item.tamanho}' if item.tamanho else ''
            linhas.append(f"• {item.quantity}x {item.product.nome}{tam_info}")
            linhas.append(f"  R$ {preco:.2f} cada = R$ {subtotal:.2f}")
            linhas.append("")

        linhas.append("━" * 20)
        linhas.append(f"*TOTAL: R$ {total:.2f}*")
        linhas.append("")
        linhas.append("✅ *Dados do Cliente:*")

        if cart.user and cart.user.is_authenticated:
            linhas.append(f"Nome: {cart.user.get_full_name() or cart.user.username}")
            linhas.append(f"Email: {cart.user.email}")
        else:
            linhas.append("Cliente: Visitante (não logado)")

        return "\n".join(linhas)