from .views import *
from django.urls  import path, include

urlpatterns = [
    path('/signup', SignupView.as_view()),
    path('/login', LoginView.as_view()),
    path('/find', FindmemberView.as_view())
]