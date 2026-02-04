from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save, m2m_changed

from produtos.models import Produto

user = settings.AUTH_USER_MODEL

class CartManager(models.Manager):
    def new_or_get(self, request):
        user = request.user
        cart = None
        created = False

    
        if user.is_authenticated:
            cart_qs = self.get_queryset().filter(user=user)

            if cart_qs.exists():
                cart = cart_qs.first()
            else:
                cart = self.create(user=user)
                created = True

            request.session["cart_id"] = cart.id
            return cart, created

        
        cart_id = request.session.get("cart_id")

        if cart_id:
            cart_qs = self.get_queryset().filter(id=cart_id, user__isnull=True)
            if cart_qs.exists():
                return cart_qs.first(), False

        cart = self.create()
        request.session["cart_id"] = cart.id
        return cart, True

               




class Cart(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE, null = True, blank = True)
    products = models.ManyToManyField(Produto, blank = True)
    total = models.DecimalField(default = 0.00, max_digits=19, decimal_places = 2)
    subtotal = models.DecimalField(default=0.00, max_digits=19, decimal_places=2)
    updated = models.DateTimeField(auto_now = True)
    timestamp = models.DateTimeField(auto_now_add = True)


    objects = CartManager()

    def _str_(self):
        return str(self.id)
    

def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        products = instance.products.all()
        total = 0
        for product in products:
            total += product.preco
            print(total)
        if instance.subtotal != total:
            instance.subtotal = total
            instance.save()


m2m_changed.connect(m2m_changed_cart_receiver, sender = Cart.products.through)

def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    if instance.subtotal > 0:
        instance.total = instance.subtotal # considere o 10 como uma taxa de entrega
    else:
        instance.total = 0.00

pre_save.connect(pre_save_cart_receiver, sender = Cart)