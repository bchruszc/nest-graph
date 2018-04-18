from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from nest_graph.models import Device, DeviceState
from datetime import datetime, date

import nest
import uuid
import json

client_id = 'e639b04d-d513-4d54-b54a-6848a737cbfc'
client_secret = 'jXKit8QM0ySq7z8dlkK65hvPX'


@login_required
def dashboard(request):
    template = loader.get_template('nest_graph/overview.html')

    # Get the last day of states

    # Convert states to 3 columns: x (timestamp), Temperature, Target

    # TODO:  Load the correct states for this user/device
    # Convert the timestamps and stuff to json
    # Pass json to browser
    # Test that the json looks right
    # Repeat for ranges
    states = DeviceState.objects.filter(state_timestamp__date=date(2018, 3, 23))

    columns = states_to_graph_data(states)
    ranges = states_to_graph_ranges(states)

    context = {
        'page_header': 'Page Header.',
        'user_profile': request.user.profile,
        'devices': request.user.profile.devices.all(),
        'graph_columns': columns,
        'graph_regions': ranges
    }
    return HttpResponse(template.render(context, request))


# Need to convert the histories in to d3 consumable data.  Simple python dicts converted to a json string
def states_to_graph_data(states):
    xs = ['x']
    temps = ['Temperature']
    targets = ['Target']

    for s in states:
        x = s.state_timestamp.strftime("%y-%m-%d %H:%M:%S")
        temp = s.temperature
        target = s.target

        xs.append(x)
        temps.append(temp)
        targets.append(target)

    def json_serial(obj):
        """JSON serializer for objects not serializable by default json code"""

        if isinstance(obj, (datetime, date)):
            serial = obj.timestamp()
            return serial
        raise TypeError("Type %s not serializable" % type(obj))

    columns = [xs, targets, temps]

    return json.dumps(columns, default=json_serial)


# Need to convert the histories in to d3 consumable data.  Simple python dicts converted to a json string
def states_to_graph_ranges(states):
    ranges = []

    current_value = None
    range_start = None
    range_end = None

    for s in states:

        range_end = s.state_timestamp.strftime("%y-%m-%d %H:%M:%S")

        if current_value == s.hvac_state:
            # Keep on keeping on
            continue
        else:
            # End the old range if necessary, and start a new range
            if range_start:
                ranges.append({'start': range_start, 'end': range_end, 'class': ('graph-' + current_value)})

            range_start = s.state_timestamp.strftime("%y-%m-%d %H:%M:%S")

        current_value = s.hvac_state

    if range_end:   # Handle case where there are no points
        ranges.append({'start': range_start, 'end': range_end, 'class': ('graph-' + current_value)})

    def json_serial(obj):
        """JSON serializer for objects not serializable by default json code"""

        if isinstance(obj, (datetime, date)):
            serial = obj.timestamp()
            return serial
        raise TypeError("Type %s not serializable" % type(obj))

    return json.dumps(ranges, default=json_serial)


@login_required
def devices(request):
    request.user.profile.nest_oauth_state = str(uuid.uuid4())  # 36 chars (e.g. 16fd2706-8baf-433b-82eb-8c7fada847da)
    request.user.profile.save()
    request.user.save()

    template = loader.get_template('nest_graph/devices.html')
    context = {
        'page_header': 'Page Header.',
        'user_profile': request.user.profile,
        'devices': request.user.profile.devices.all(),
        'oauth_state': request.user.profile.nest_oauth_state,
    }
    return HttpResponse(template.render(context, request))


# This call should only be initiated by the Nest API
# @see https://developers.nest.com/documentation/cloud/how-to-auth
@login_required
def nest_callback(request):
    # Collect info

    # Exchange token for code via another call

    # Redirect to devices page

    # request.user.profile.nest_oauth_state = '4' # TODO: Generate GUID
    # request.user.profile.save()
    #

    profile = request.user.profile

    # Check that the state is what we expect for this user
    if request.GET['state'] != profile.nest_oauth_state:
        return HttpResponse('Unauthorized token', status=401)

    # Use the code to fetch a token
    code = request.GET['code']
    napi = nest.Nest(client_id=client_id, client_secret=client_secret)
    napi.request_token(code)
    profile.nest_oauth_token = napi.access_token

    profile.devices.all().delete()  # TODO: Shouldn't delete every time....  just check for new?

    for t in napi.thermostats:
        d = Device()
        d.user_profile = profile
        d.name = t.name
        d.device_id = t.device_id
        d.save()

        profile.devices.add(d)

    # Save the token to the user profile
    profile.save()

    template = loader.get_template('nest_graph/devices.html')
    context = {
        'page_header': 'Page Header.',
        'user_profile': profile,
        'devices': profile.devices.all(),
        'oauth_state': profile.nest_oauth_state,
    }
    return HttpResponse(template.render(context, request))


@login_required
def remove_profile(request):
    request.user.profile.nest_account = None
    request.user.profile.devices.delete()
    request.user.profile.save()

    template = loader.get_template('nest_graph/devices.html')
    context = {
        'page_header': 'Page Header.',
        'user_profile': request.user.profile,
        'devices': request.user.profile.devices.all(),
    }
    return HttpResponse(template.render(context, request))
