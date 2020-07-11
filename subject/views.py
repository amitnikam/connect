from .models import Subject
from django.views.generic import ListView
from django.db.models import Q


class SubjectListView(ListView):
    model = Subject
    context_object_name = 'subjects'

    def get_queryset(self):
        query = self.request.GET.get("q", None)
        if query is not None:
            return Subject.objects.filter(Q(code__icontains=query) | Q(name__icontains=query) | Q(keywords__icontains=query))
        else:
            return Subject.objects.all()
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "All Subjects"
        return context

