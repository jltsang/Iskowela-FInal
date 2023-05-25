from django.shortcuts import render, redirect, get_object_or_404
from main.models import Toggles
import requests
from django.utils import timezone
from .models import Monitor, TimeTracking
from django.core.paginator import Paginator
import datetime
from django.contrib.gis.geoip2 import GeoIP2
from django.db.models import Count
from users.models import Profile
import json
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from geoip2.errors import AddressNotFoundError

@csrf_exempt
def update_time_spent(request):
   if request.method == 'POST':
        # Get the TimeTracking object for the current page
        try:
            time_tracking = TimeTracking.objects.order_by('-last_update').first()
        except TimeTracking.DoesNotExist:
            return JsonResponse({'status': 'error'})

        # Calculate the time spent on the page
        time_spent = (timezone.now() - time_tracking.last_update).total_seconds()

        # Update the TimeTracking object
        time_tracking.time_spent += time_spent
        time_tracking.last_update = timezone.now()
        time_tracking.save()

        return JsonResponse({'status': 'success'})
   else:
        return JsonResponse({'status': 'error'})



@login_required
def traffic_monitor(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)

    if profile.user != request.user:
        return render(request, '403.html', status=403)
    
    dataSaved = Monitor.objects.filter(profile = profile_id).order_by('-datetime')

    p = Paginator(dataSaved, 10)
    pageNum = request.GET.get('page', 1)
    page = p.page(pageNum)

    data = {
        "now":timezone.now(),
        "unique":Monitor.objects.filter(profile = profile_id).values('ip').distinct().count(),
        "totalSiteVisits":dataSaved.count(),
        "courseVisits": Monitor.objects.filter(page_visited = "course", profile = profile_id).count(),
        "processVisits": Monitor.objects.filter(page_visited = "process", profile = profile_id).count(),
        "scholarshipVisits": Monitor.objects.filter(page_visited = "scholarship", profile = profile_id).count(),
        "markerVisits": Monitor.objects.filter(page_visited = "markers", profile = profile_id).count(),
        "chatbotVisits": Monitor.objects.filter(page_visited = "chatbot", profile = profile_id).count(),
        "userSession": page,
    }

    charts = chart(request, profile_id)
    context = {
        'active_profile': Profile.objects.get(id=profile_id),
		'toggles': Toggles.objects.get(profile = profile_id),
        'data': data,
        'profile_id': profile_id,
        'charts': charts,
	}
   

    return render(request, 'analytics/traffic_monitor.html', context)

def get_session(request, profile_id, page):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR') 
    if ip == '127.0.0.1': # Only define the IP if you are testing on localhost.
        ip = '202.92.130.117'

    g = GeoIP2()
    try:
        location = g.city(ip)
        continent = location.get("continent_name")
        country = location.get("country_name")
        city = location.get("city")
    except AddressNotFoundError:
        continent = "Unknown"
        country = "Unknown"
        city = "Unknown"

    profile = Profile.objects.get(id=profile_id)
    saveNow = Monitor(
        profile=profile,
        continent=continent,
        country=country,
        city=city,
        datetime=timezone.now(),
        ip=ip,
        page_visited=page
    )
    saveNow.save()
    

def chart(request, profile_id):
    # Per Module View Data
    course = Monitor.objects.filter(page_visited = "course", profile = profile_id).count()
    course = int(course)
   
    scholarship = Monitor.objects.filter(page_visited = "scholarship", profile = profile_id).count()
    scholarship = int(scholarship)

    process = Monitor.objects.filter(page_visited = "process", profile = profile_id).count()
    process = int(process)

    chatbot = Monitor.objects.filter(page_visited = "chatbot", profile = profile_id).count()
    chatbot = int(chatbot)

    markers = Monitor.objects.filter(page_visited = "markers", profile = profile_id).count()
    markers = int(markers)


    # Visitor Location Data
    cities = Monitor.objects.filter(profile = profile_id).values('city').distinct()
    city_list = list(cities.values_list('city',flat=True))
    city_count = [Monitor.objects.filter(profile = profile_id, city=city).count() for city in city_list]


    # Overall site visit
    today = timezone.now()
    start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_of_month = start_of_month.replace(month=start_of_month.month+1)-timezone.timedelta(microseconds=1)

    data = (
        Monitor.objects
        .filter(profile = profile_id, datetime__gte=start_of_month, datetime__lte=end_of_month)
        .values('datetime__date')
        .annotate(ip_count=Count('ip'))
        .order_by('datetime__date')
    )
    
    # Time Spent Per Module View Data
    course_time = TimeTracking.objects.filter(page__contains="{}/courses/".format(profile_id)).aggregate(Sum('time_spent'))['time_spent__sum']
    scholarship_time = TimeTracking.objects.filter(page__icontains="{}/scholarships/".format(profile_id)).aggregate(Sum('time_spent'))['time_spent__sum']
    process_time = TimeTracking.objects.filter(page__icontains="{}/processguides/".format(profile_id)).aggregate(Sum('time_spent'))['time_spent__sum']
    chatbot_time = TimeTracking.objects.filter(page__icontains="{}/chatbot/".format(profile_id)).aggregate(Sum('time_spent'))['time_spent__sum']
    marker_time = TimeTracking.objects.filter(page__icontains="{}/markers/".format(profile_id)).aggregate(Sum('time_spent'))['time_spent__sum']
    


    page_list = []
    page_count = []
    time_spent = []

    toggles = Toggles.objects.get(profile=profile_id)
    if toggles.courses_toggle == True:
        page_list.append('Courses')
        page_count.append(course)
        time_spent.append(course_time)
    if toggles.processguides_toggle == True:
        page_list.append('Process Guides')
        page_count.append(process)
        time_spent.append(process_time)
    if toggles.processguides_toggle == True:
        page_list.append('Scholarships')
        page_count.append(scholarship)
        time_spent.append(scholarship_time)
    if toggles.chatbot_toggle == True:
        page_list.append('Chatbot')
        page_count.append(chatbot)
        time_spent.append(chatbot_time)
    if toggles.markers_toggle == True:
        page_list.append('Events/Places')
        page_count.append(markers)
        time_spent.append(marker_time)
    
    
    context = {'page_list':page_list, 'page_count':page_count, 'country_list': city_list, 'country_count': city_count, 'data': data, 'time_spent': time_spent}
    return context