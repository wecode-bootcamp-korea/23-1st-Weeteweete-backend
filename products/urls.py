from django.urls  import path
from products.views  import MenuPageView

urlpatterns = [
    path('', MenuPageView.as_view()),
] 