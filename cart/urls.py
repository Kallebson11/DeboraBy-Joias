from django.urls import path
from .views import CartHomeView, CartUpdateView

app_name = "carts"

urlpatterns = [
    path("", CartHomeView.as_view(), name="home"),
    path("update/", CartUpdateView.as_view(), name="update"),
]
