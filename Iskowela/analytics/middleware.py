from django.utils import timezone
from .models import TimeTracking


class TimeTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Only track time for GET requests
        if request.method == 'GET':
            # Check if the user is authenticated
            if request.user.is_authenticated:
                # Get or create the TimeTracking object
                try:
                    time_tracking = TimeTracking.objects.get(user=request.user, page=request.path)
                except TimeTracking.DoesNotExist:
                    time_tracking = TimeTracking(user=request.user, page=request.path)

                # Record the current time
                time_tracking.start_time = timezone.now()
                time_tracking.last_update = timezone.now()
                time_tracking.save()

                # Add a cookie with the ID of the TimeTracking object
                response.set_cookie('time_tracking_id', time_tracking.id)

        return response
    
