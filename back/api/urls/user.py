from django.urls import path

from api.views.user import user_info_by_token, sign_up, log_in, log_out, send_secret_key, \
    password_reset, profile, Details, List, send_email

urlpatterns = [
    path('users/', List.as_view()),
    path('users/<int:pk>/', Details.as_view()),
    path('users/<int:pk>/profile/', profile),
    path('userInfoByToken/', user_info_by_token),
    path('signUp/', sign_up),
    path('logIn/', log_in),
    path('logOut/', log_out),
    path('sendSecretKey/', send_secret_key),
    path('emailByUsername/', send_email),
    path('passwordReset/', password_reset)
]