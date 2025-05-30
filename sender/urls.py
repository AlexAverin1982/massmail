from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("new_client/", views.ClientCreateView.as_view(), name="new_client"),
    path("client_details/<int:pk>/", views.ClientDetailView.as_view(), name="client_details"),
    path("edit_client/<int:pk>/", views.ClientUpdateView.as_view(), name="edit_client"),
    path("delete_client/<int:pk>/", views.ClientDeleteView.as_view(), name="delete_client"),
]
"""
path("", views.ClientListView.as_view(), name="home"),
path("details/<int:pk>/", views.ClientDetailView.as_view(), name="client_details"),
path("new_client/", views.ClientCreateView.as_view(), name="new_client"),
path("edit/<int:pk>/", views.ClientUpdateView.as_view(), name="edit_client"),
path("new_category/", views.CategoryCreateView.as_view(), name="new_category"),
path("contacts/", views.ContactsView.as_view(), name="contacts"),
path("feedback/", views.FeedbackFormView.as_view(), name="feedback"),
path("posted_info/<int:pk>/", views.PostedMessageView.as_view(), name="posted_info"),
path("delete/<int:pk>/", views.ClientDeleteView.as_view(), name="delete_client"),
path("send_letter/", views.send_letter, name="send_letter"),
path("category_clients/<int:pk>/", views.CategoryClientsListView.as_view(), name="category_clients"),
"""
