from django.urls import path
from .views import RegisterView, RetrieveUserView, AgentListView


urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("", RetrieveUserView.as_view()),
    path("agents/", AgentListView.as_view()),
]
