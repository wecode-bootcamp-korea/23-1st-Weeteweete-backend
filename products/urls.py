from django.urls  import path
from products.views  import MenuPageView

urlpatterns = [
    path('/menu', MenuPageView.as_view()),
] 