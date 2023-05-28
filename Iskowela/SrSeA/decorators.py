from django.shortcuts import redirect
from django.urls import reverse_lazy
from main.models import Toggles  # Import the model that contains the toggle value

def toggle_required(function, toggle_name):
    def wrap(request, profile_id, *args, **kwargs):
        # Get the toggle value for the specific profile_id from the database
        toggles = Toggles.objects.get(profile_id=profile_id).__dict__[toggle_name]
        if toggles is False:
            # Redirect to a specific URL if the toggle value is false
            return redirect(reverse_lazy('portal'))  # Replace 'toggle_off' with the URL name or path

        return function(request, profile_id, *args, **kwargs)

    return wrap
