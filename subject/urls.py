from django.urls import path
from blog.views import SubjectPostListView
from .views import SubjectListView

urlpatterns = [
    path('', SubjectListView.as_view(), name='subject-all'),
    path('<code>/', SubjectPostListView.as_view(), name='subject-profile'),
]
