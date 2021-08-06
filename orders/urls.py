from django.urls  import path
from .views       import OrderView, PurchaseView

urlpatterns = [
    path('/<int:item_id>', OrderView.as_view()),
    path('', OrderView.as_view()),
    path('/purchase', PurchaseView.as_view()),
]