from django.urls  import path
from products.views  import MenuPageView, MainPageView

urlpatterns = [
    path('', MenuPageView.as_view()),
    path('/main', MainPageView.as_view()),
] 