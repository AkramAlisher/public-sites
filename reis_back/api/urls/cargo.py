from django.urls import path

from api.views.cargo import List, Details, send_to_email, my, search, pinned

urlpatterns = [
    path('cargo/', List.as_view()),
    path('cargo/<int:pk>/', Details.as_view()),
    path('cargo/search/', search),
    path('cargo/pinned/', pinned),
    path('cargo/my/', my),
    path('cargo/sendToEmail/', send_to_email),
]