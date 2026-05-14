from django.conf import settings
from django.db import models
from produtos.models import Produto

User = settings.AUTH_USER_MODEL


# ============================================================
# GERENCIADOR DO CARRINHO
# ============================================================

class CartManager(models.Manager):

    def new_or_get(self, request):
        user = request.user
        if user.is_authenticated:
            cart, created = self.get_queryset().get_or_create(user=user)
            return cart, created
        return Cart(), False

    def get_or_create_for_request(self, request):
        user = request.user
        if user.is_authenticated:
            cart, created = self.get_queryset().get_or_create(user=user)
            return cart, created
        return None, False


# ============================================================
# ITEM DO CARRINHO
# ============================================================

class CartItem(models.Model):
    cart     = models.ForeignKey('Cart', on_delete=models.CASCADE)
    product  = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    tamanho  = models.CharField(max_length=20, blank=True, null=True,
                                verbose_name='Tamanho')
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        tam = f' — {self.tamanho}' if self.tamanho else ''
        return f'{self.quantity} x {self.product.nome}{tam}'

    def get_total_price(self):
        return self.quantity * self.product.preco

    class Meta:
        # Permite o mesmo produto com tamanhos diferentes no mesmo carrinho
        unique_together = ('cart', 'product', 'tamanho')


# ============================================================
# CARRINHO
# ============================================================

class Cart(models.Model):
    user      = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    items     = models.ManyToManyField(Produto, through='CartItem', blank=True)
    updated   = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CartManager()

    def __str__(self):
        if self.user:
            return f'Carrinho {self.id} — {self.user}'
        return f'Carrinho {self.id} — Anônimo'

    @property
    def subtotal(self):
        return sum(item.get_total_price() for item in self.cartitem_set.all())

    @property
    def total(self):
        return self.subtotal

    def add_product(self, product, quantity=1, tamanho=None):
        """Adiciona produto ou incrementa quantidade se já existir."""
        cart_item, created = CartItem.objects.get_or_create(
            cart=self,
            product=product,
            tamanho=tamanho or None,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        return cart_item

    def remove_product(self, product, quantity=1, tamanho=None):
        """Remove produto (com tamanho específico) ou decrementa quantidade.
        Se tamanho não for informado, remove o primeiro item encontrado.
        """
        qs = CartItem.objects.filter(cart=self, product=product)
        if tamanho:
            qs = qs.filter(tamanho=tamanho)
        cart_item = qs.first()
        if not cart_item:
            return
        if cart_item.quantity <= quantity:
            cart_item.delete()
        else:
            cart_item.quantity -= quantity
            cart_item.save()

    def get_product_quantity(self, product):
        try:
            return CartItem.objects.get(cart=self, product=product).quantity
        except CartItem.DoesNotExist:
            return 0

    def get_cart_items(self):
        if not self.pk:
            return CartItem.objects.none()
        return self.cartitem_set.all()

    def clear_cart(self):
        if self.pk:
            self.cartitem_set.all().delete()