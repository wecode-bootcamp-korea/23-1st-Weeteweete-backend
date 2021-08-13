from django.urls     import path
from products.views  import PageView, DetailPageView, ReviewView

urlpatterns = [
    path('', PageView.as_view()),
    path('/<int:item_id>', DetailPageView.as_view()),
    path('/review/<int:item_id>', ReviewView.as_view())
] 