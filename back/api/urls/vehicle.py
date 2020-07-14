from django.urls import path

from api.views.vehicle import List, Details, search, pinned, my, send_to_email

urlpatterns = [
    path('vehicle/', List.as_view()),
    path('vehicle/<int:pk>/', Details.as_view()),
    path('vehicle/search/', search),
    path('vehicle/pinned/', pinned),
    path('vehicle/my/', my),
    path('vehicle/sendToEmail/', send_to_email),
]