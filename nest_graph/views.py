from django.http import HttpResponse
from django.template import loader

from nest_graph.models import DeviceState

import nest
import pickle
import datetime

def dashboard(request):
    if request.user.is_authenticated():
        template = loader.get_template('nest_graph/overview.html')
        context = {
            'page_header' : 'Page Header.',
            'user_profile': request.user.profile,
            'devices': request.user.profile.devices,
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponse("You're not logged in.")

