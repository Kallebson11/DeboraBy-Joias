from django.urls import path
from .views import CartHomeView, CartUpdateView, CartRemoveItemView, CartClearView, CartWhatsAppView

app_name = "carts"

urlpatterns = [
    path("",         CartHomeView.as_view(),    name="home"),
    path("update/",  CartUpdateView.as_view(),  name="update"),
    path("remove/",  CartRemoveItemView.as_view(), name="remove"),
    path("clear/",   CartClearView.as_view(),   name="clear"),
    path("whatsapp/",CartWhatsAppView.as_view(),name="whatsapp"),
]