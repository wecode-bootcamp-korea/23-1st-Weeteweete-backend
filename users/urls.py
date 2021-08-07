
from users.views  import SignUpView, LoginView, FindMemberView, NewPasswordView

urlpatterns = [
    path('/singup', SignUpView.as_view()),
    path('/singin', LoginView.as_view()),
    path('/account', FindMemberView.as_view()),
    path('/password', NewPasswordView.as_view()),
]