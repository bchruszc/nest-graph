from django.core.management.base import BaseCommand
from nest_graph.models import DeviceState
from django.contrib.auth.models import User

import nest
import pickle
import datetime
import base64

class Command(BaseCommand):
    def _read_nest(self):
        for u in User.objects.all():
            for d in u.profile.devices.all():
                napi = nest.Nest(u.profile.nest_username, u.profile.nest_password)
                
                # napi._status is essentially the raw data, in case we want is again laster
#                print 'Starting Nest read...'
            
                ds = DeviceState()
                
                ds.device = d
                
                ds.state_pickle = base64.b64encode(pickle.dumps(napi._status))
                ds.weather_pickle = base64.b64encode(pickle.dumps(napi.structures[0].weather))
                
                # Timestamp from when the state snapshot was taken
                ds.state_timestamp = datetime.datetime.now()
                
                # Fields that are likely of greatest interest
                device = napi.devices[0]
                
                ds.name = device.name
                ds.where = device.where
                ds.mode = device.mode
                ds.fan = device.fan
                ds.temperature = device.temperature
                ds.humidity = device.humidity
                ds.target = device.target
                ds.away_heat = device.away_temperature[0]
                ds.away_cool = device.away_temperature[1]
                
                ds.hvac_ac_state = device.hvac_ac_state
                ds.hvac_cool_x2_state = device.hvac_cool_x2_state
                ds.hvac_heater_state = device.hvac_heater_state
                ds.hvac_aux_heater_state = device.hvac_aux_heater_state
                ds.hvac_heat_x2_state = device.hvac_heat_x2_state
                ds.hvac_heat_x3_state = device.hvac_heat_x3_state
                ds.hvac_alt_heat_state = device.hvac_alt_heat_state
                ds.hvac_alt_heat_x2_state = device.hvac_alt_heat_x2_state
                ds.hvac_emer_heat_state = device.hvac_emer_heat_state
                
                ds.online = device.online
                ds.last_ip = device.last_ip
                ds.local_ip = device.local_ip
                ds.last_connection = device.last_connection
                
                ds.save()
    
    
    
                
    def handle(self, *args, **options):
        self._read_nest()
        

    '''
    temperature = models.FloatField()
    humidity = models.FloatField()
    target = models.FloatField()
    away_heat = models.FloatField()
    away_cool = models.FloatField()
    
    hvac_ac_state = models.BooleanField()
    hvac_cool_x2_state = models.BooleanField()
    hvac_heater_state = models.BooleanField()
    hvac_aux_heater_state = models.BooleanField()
    hvac_heat_x2_state = models.BooleanField()
    hvac_heat_x3_state = models.BooleanField()
    hvac_alt_heat_state = models.BooleanField()
    hvac_alt_heat_x2_state = models.BooleanField()
    hvac_emer_heat_state = models.BooleanField()
    
    online = models.BooleanField()
    last_ip = models.CharField(max_length=100)
    local_ip = models.CharField(max_length=100)
    last_connection = models.CharField(max_length=100)
    
    error_code = models.CharField(max_length=100)
    battery_level = models.CharField(max_length=100)   
    '''
    
    
    
    
    
    '''
    for k in dir(napi):
        #print k
        #if k[0] != '_':
        try:
            contents += '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp%s: %s<br>' % (k, str(getattr(napi, k)))
        except:
            contents += '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp%s: %s<br>' % (k, 'Unknown')


       
        for structure in napi.structures:
            print 'S: ' + str(structure.address)
            contents += 'Structure %s' % structure.name + '<br>'
            contents += '&nbsp&nbsp&nbsp&nbspAway: %s' % structure.away + '<br>'
            contents += '&nbsp&nbsp&nbsp&nbspDevices:' + '<br>'
    ''' 
   
