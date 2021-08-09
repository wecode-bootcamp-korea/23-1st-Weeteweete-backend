from django.urls     import path
from products.views  import PageView, DetailPageView

urlpatterns = [
    path('', PageView.as_view()),
    path('/<int:item_id>', DetailPageView.as_view()),
] 