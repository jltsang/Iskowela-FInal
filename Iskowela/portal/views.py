from django.shortcuts import render
from django.views.generic import ListView
from users.models import Profile
from django.db.models import Q

class SchoolListView(ListView):
	model = Profile
	paginate_by = 15
	template_name = 'portal/portal.html'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['profiles'] = Profile.objects.all()
		return context
	
class SchoolSearchListView(ListView):
    model = Profile
    template_name = 'portal/portal.html'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            return Profile.objects.filter(Q(school_name__icontains=query) | Q(location__icontains=query) | Q(courses__course_list__icontains=query) ).distinct()
        else:
            return Profile.objects.all()