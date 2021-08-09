from django.urls import path
from users.views  import SignUpView, SignInView, FindMemberView, NewPasswordView

urlpatterns = [
    path('/singup', SignUpView.as_view()),
    path('/singin', SignInView.as_view()),
    path('/account', FindMemberView.as_view()),
    path('/password', NewPasswordView.as_view()),
]