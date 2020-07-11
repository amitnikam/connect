from django.urls import path
from blog.views import UserPostListView
from .views import UserListView

urlpatterns = [
    path('', UserListView.as_view(), name='user-all'),
    path('<username>/', UserPostListView.as_view(), name='user-profile'),
]