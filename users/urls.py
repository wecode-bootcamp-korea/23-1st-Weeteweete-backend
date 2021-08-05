from django.urls  import path
from users.views  import SignUpView, LoginView

urlpatterns = [
    path('/member/new', SignUpView.as_view()),
    path('/member', LoginView.as_view()),
]