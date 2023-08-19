from django.urls import path
from .views import (
    ManagePropertyView,
    PropertyDetailView,
    PropertyListView,
    SearchPropertyView,
)

urlpatterns = [
    path("manage/", ManagePropertyView.as_view()),
    path("detail/", PropertyDetailView.as_view()),
    path("", PropertyListView.as_view()),
    path("search/", SearchPropertyView.as_view()),
]
