from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("new_client/", views.ClientCreateView.as_view(), name="new_client"),
    path("client_details/<int:pk>/", views.ClientDetailView.as_view(), name="client_details"),
    path("edit_client/<int:pk>/", views.ClientUpdateView.as_view(), name="edit_client"),
    path("delete_client/<int:pk>/", views.ClientDeleteView.as_view(), name="delete_client"),
    path("new_message/", views.MessageCreateView.as_view(), name="new_message"),
    path("message_details/<int:pk>/", views.MessageDetailView.as_view(), name="message_details"),
    path("edit_message/<int:pk>/", views.MessageUpdateView.as_view(), name="edit_message"),
    path("delete_message/<int:pk>/", views.MessageDeleteView.as_view(), name="delete_message"),
]
