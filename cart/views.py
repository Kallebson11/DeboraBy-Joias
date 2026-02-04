from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from produtos.models import Produto
from .models import Cart


class CartHomeView(View):
    def get(self, request):
        cart_obj, _ = Cart.objects.new_or_get(request)
        return render(request, "cart/home.html", {
            "cart": cart_obj
        })




class CartUpdateView(View):
    def post(self, request):
        product_id = request.POST.get("product_id")

        if not product_id:
            return redirect("carts:home")

        product = get_object_or_404(Produto, id=product_id)
        cart_obj, _ = Cart.objects.new_or_get(request)

        if product in cart_obj.products.all():
            cart_obj.products.remove(product)
        else:
            cart_obj.products.add(product)
        request.session['cart_items'] = cart_obj.products.count()

        return redirect("carts:home")





