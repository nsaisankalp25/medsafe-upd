from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import TabletForm, UserTabletForm
from .models import Tablet, UserTablet
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
import json
# Create your views here.
def index(request):
    return HttpResponse("Hello World")


@login_required
def add_tablet(request):
    tablet_form = TabletForm()
    if request.method == 'POST':
        form = TabletForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect to a success page or list of tablets
    else:
        form = TabletForm()
    return render(request, 'notify/add_tablet.html', {'tablet_form': tablet_form})

@login_required
def record_user_tablet(request):
    form = UserTabletForm(request.POST or None)  # Handle both GET and POST
    if request.method == 'POST' and form.is_valid():
        form.instance.user = request.user  # Set the current user
        form.save()
        return redirect('dashboard')  # Redirect to a success page or list of user-tablets
    
    # Pass the form instance (bound or unbound) to the template
    return render(request, 'notify/record_tablet.html', {'user_tablet_form': form})


@login_required
def dashboard(request):
    tablets = Tablet.objects.all()
    user_tablets = UserTablet.objects.filter(user=request.user)

    # Format the UserTablet data for alarms (you can adjust this if needed)
    user_tablets_data = [
        {
            'tablet_name': user_tablet.tablet.name,
            'alarm_time': user_tablet.alarm_time.strftime('%H:%M')  # Formatting alarm_time to HH:MM
        }
        for user_tablet in user_tablets
    ]
    
    # Convert the list to JSON format
    user_tablets_json = json.dumps(user_tablets_data, cls=DjangoJSONEncoder)

    tablet_form = TabletForm()
    user_tablet_form = UserTabletForm()

    context = {
        'tablets': tablets,
        'user_tablets': user_tablets,
        'tablet_form': tablet_form,
        'user_tablet_form': user_tablet_form,
        'user': request.user,
        'user_tablets_json': user_tablets_json  # Pass the serialized alarms to the template
    }

    return render(request, 'notify/dashboard.html', context)
