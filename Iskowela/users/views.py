from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from .models import Profile, User
from main.models import Toggles
from django.urls import reverse_lazy
from django.http import Http404

@login_required #Must be signed in (as admin) in order to create new admin accounts
def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Account created for {username}!')
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request, 'users/register.html', {'form': form})

def profile(request, profile_id):
	context = {
		'title': 'About',
		'active_profile': Profile.objects.get(id =profile_id),
		'toggles': Toggles.objects.get(profile = profile_id),
		'profile_id': profile_id,
	}
	return render(request, 'users/profile.html', context)

# Profile Update
def pupdate(request, profile_id):
	if request.user.id != Profile.objects.get(id=profile_id).user_id:
		raise Http404("You are not allowed to edit this profile")
	
	if request.method == 'POST':
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=Profile.objects.get(id=profile_id))
		u_form = UserUpdateForm(request.POST, instance=User.objects.get(id=Profile.objects.get(id=profile_id).user_id))
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f'Your profile has been updated!')
			return redirect(reverse_lazy('profile', kwargs={'profile_id': profile_id}))

	else:
		p_form = ProfileUpdateForm(instance=Profile.objects.get(id=profile_id))
		u_form = UserUpdateForm(instance=User.objects.get(id=Profile.objects.get(id=profile_id).user_id))

	context = {
		'u_form': u_form,
		'p_form': p_form,
		'title': 'Profile Update',
		'toggles': Toggles.objects.get(profile = profile_id),
		'profile_id': profile_id,
		'active_profile': Profile.objects.get(id = profile_id),
	}
	return render(request, 'users/pupdate.html', context)