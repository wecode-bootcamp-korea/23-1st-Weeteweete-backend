from django.urls  import path
from users.views  import SignUpView, LoginView

urlpatterns = [
    path('/singup', SignUpView.as_view()),
    path('/singin', LoginView.as_view()),
]