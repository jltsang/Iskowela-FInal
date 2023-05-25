from django.shortcuts import render
from users.models import Profile
from .models import SSR
from django.views.generic import (
	ListView, 
	CreateView,
	DeleteView
)
from django.db.models import Avg
from main.models import Toggles
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

def index(request, profile_id):
	context = {
		'title': 'Stats',
		'ratings': SSR.objects.filter(profile_id=profile_id),
		'toggles': Toggles.objects.get(profile=profile_id),
		'profile_id': profile_id,
		'active_profile': Profile.objects.get(id=profile_id),
	}
	return render(request, 'ssr/index.html', context)

class SSRListView(ListView):
	model = SSR
	template_name = 'ssr/index.html'
	context_object_name = 'ssrs'
	paginate_by = 5

	def get_queryset(self):
		return SSR.objects.filter(profile=self.kwargs['profile_id']).order_by('-date_posted')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['toggles'] = Toggles.objects.get(profile=self.kwargs['profile_id'])
		context['title'] = 'Stats'
		
		# round ratings only if they are not null
		context['average_imap'] = round(list(SSR.objects.filter(profile=self.kwargs['profile_id']).aggregate(Avg('interactive_map_rating')).values())[0], 2) if SSR.objects.filter(profile=self.kwargs['profile_id']).exists() else None
		context['average_chatbot'] = round(list(SSR.objects.filter(profile=self.kwargs['profile_id']).aggregate(Avg('chatbot_rating')).values())[0], 2) if SSR.objects.filter(profile=self.kwargs['profile_id']).exists() else None
		context['average_overall'] = round(list(SSR.objects.filter(profile=self.kwargs['profile_id']).aggregate(Avg('overall_rating')).values())[0], 2) if SSR.objects.filter(profile=self.kwargs['profile_id']).exists() else None
		context['count'] = SSR.objects.filter(profile=self.kwargs['profile_id']).count()
		context['toggles'] = Toggles.objects.get(profile_id=self.kwargs['profile_id'])    
		context['profile_id'] = self.kwargs['profile_id']
		context['active_profile'] = Profile.objects.get(id=self.kwargs['profile_id'])
		return context


class SSRCreateView(CreateView):
	model = SSR
	fields = ['email', 'interactive_map_comment', 'interactive_map_rating', 'chatbot_comment', 'chatbot_rating', 'overall_comment', 'overall_rating']
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Feedback'
		context['toggles'] = Toggles.objects.get(profile_id=self.kwargs['profile_id'])	
		context['profile_id'] = self.kwargs['profile_id']
		context['active_profile'] = Profile.objects.get(id=self.kwargs['profile_id'])

		return context

	def get_success_url(self):
		return reverse_lazy("ssr-create", kwargs={"profile_id": self.kwargs['profile_id']})
	def form_valid(self, form):
		profile = get_object_or_404(Profile, id=self.kwargs['profile_id'])
		form.instance.profile = profile
		return super().form_valid(form)

class SSRDeleteView(DeleteView):
	model = SSR
	success_url = "/ssr/"
