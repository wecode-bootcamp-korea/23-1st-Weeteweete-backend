from django.urls  import path
from .views       import OrderView, PurchaseView, CartView

urlpatterns = [
    path('', OrderView.as_view()),
    path('', CartView.as_view()),
    path('/purchase', PurchaseView.as_view()),
]