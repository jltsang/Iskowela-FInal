from django.shortcuts import render, redirect
from main.models import Toggles
from users.models import Profile
import requests
from chatbot.models import Message
from information.models import Scholarships, ProcessGuide, Courses
from markers.models import Place_Markers, Event_Markers
from analytics.views import get_session
from django.http import HttpResponse, JsonResponse
from django.db.models import Max
import time
from django.db.models import Q

def chatbot(request, profile_id):
	get_session(request, profile_id, "chatbot")
	user_id = Message.objects.filter(user_id__isnull=False).aggregate(Max('user_id'))['user_id__max']
	if user_id is None:
		user_id = 1
	else:
		user_id += 1
	Message.objects.create(value="Hello! Feel free to ask me any questions.", user_id=user_id, is_bot=True)
	return render(request, 'chatbot/chatbot.html', {
		'title': 'Chatbot',
		'profile_id': profile_id,
		'active_profile': Profile.objects.get(id=profile_id),
		'toggles': Toggles.objects.get(profile = profile_id),
		'user_id': user_id,
	})

def send(request, profile_id):
	message = request.POST['message']
	user_id = request.POST['user_id']

	new_message = Message.objects.create(value=message, user_id=user_id, is_bot=False)
	new_message.save()
    
	time.sleep(1)
	rasa_url = 'http://rasa:5005/webhooks/rest/webhook'
	payload = {
		'message': "From " + str(profile_id) + ", " + message,
		'sender': user_id
	}
	response = requests.post(rasa_url, json=payload)
	rasa_response = response.json()

	# Save Rasa's response
	for message in rasa_response:
		new_message = Message.objects.create(value=message['text'], user_id=user_id, is_bot=True)
		new_message.save()

	return HttpResponse('Message sent successfully')

def getMessages(request, user_id):
	messages = Message.objects.filter(user_id=user_id)

	return JsonResponse({"messages":list(messages.values())})

def queryScholarships(request, school_id, scholarship_name=None):
	if scholarship_name is None:
		scholarships = Scholarships.objects.filter(profile=Profile.objects.get(id=school_id))
		return JsonResponse({"scholarships":list(scholarships.values())})
	else:
		scholarship = Scholarships.objects.filter(
			Q(profile=Profile.objects.get(id=school_id)) &
			Q(scholarship_name__icontains=scholarship_name)
		)
		return JsonResponse({"scholarships":list(scholarship.values())})

def queryProcessGuides(request, school_id, process_name=None):
	if process_name is None:
		processes = ProcessGuide.objects.filter(profile=Profile.objects.get(id=school_id))
		return JsonResponse({"processes":list(processes.values())})
	else:
		if process_name is int:
			process = ProcessGuide.objects.filter(
				Q(profile=Profile.objects.get(id=school_id)) &
				Q(apply=process_name)
			)
		else:
			process = ProcessGuide.objects.filter(
				Q(profile=Profile.objects.get(id=school_id)) &
				Q(process_name__icontains=process_name)
			)
		return JsonResponse({"processes":list(process.values())})

def queryCourses(request, school_id, college_group=None):
    if college_group is None:
        courses = Courses.objects.filter(profile=Profile.objects.get(id=school_id))
        return JsonResponse({"courses":list(courses.values())})
    else:
        course = Courses.objects.filter(
            Q(profile=Profile.objects.get(id=school_id)) &
            Q(college_group__icontains=college_group)
        )
        return JsonResponse({"courses":list(course.values())})

def queryPlaces(request, school_id, place_name=None):
	if place_name is None:
		places = Place_Markers.objects.filter(profile=Profile.objects.get(id=school_id))
		return JsonResponse({"places":list(places.values())})
	else:
		place = Place_Markers.objects.filter(
			Q(profile=Profile.objects.get(id=school_id)) &
			Q(name__icontains=place_name)
		)
		return JsonResponse({"places":list(place.values())})

def queryPlacesByType(request, school_id, place_type):
    place_type_choices = {
        'health': Place_Markers.PlaceType.HEALTH,
        'food': Place_Markers.PlaceType.FOOD,
        'finance': Place_Markers.PlaceType.FINANCE,
        'store': Place_Markers.PlaceType.STORE,
        'other': Place_Markers.PlaceType.ETC,
    }

    if place_type.lower() not in place_type_choices:
        return JsonResponse({"error": "Invalid place type."})

    places = Place_Markers.objects.filter(
        Q(profile=Profile.objects.get(id=school_id)) &
        Q(type=place_type_choices[place_type.lower()])
    )
    return JsonResponse({"places": list(places.values())})

def queryEvents(request, school_id, event_name=None):
	if event_name is None:
		events = Event_Markers.objects.filter(profile=Profile.objects.get(id=school_id))
		return JsonResponse({"events":list(events.values())})
	else:
		event = Event_Markers.objects.filter(
			Q(profile=Profile.objects.get(id=school_id)) &
			Q(name__icontains=event_name)
		)
		return JsonResponse({"events":list(event.values())})