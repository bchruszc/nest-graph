from django.db import models
from django.contrib.auth.models import User
#from nest_graph import settings

class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    
    friendly_name = models.CharField(max_length=40, default='Friend')
    
    nest_username = models.CharField(max_length=40, default='')
    nest_password = models.CharField(max_length=40, default='') #, widget=models.PasswordInput)

    def __str__(self):
        return '%s (%s)' % (self.friendly_name, self.user.username)


class Device(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='devices')
    device_name = models.CharField(max_length=40, default='NEST')

    def __str__(self):
        return '%s''s device: %s' % (self.user_profile.friendly_name, self.device_name)


class DeviceState(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='states')

    # A pickled representation of the 'raw' Nest response provided by our libraries
    state_pickle = models.CharField(max_length=100000, default='')
    
    # A pickled version of the complete weather object
    weather_pickle = models.CharField(max_length=100000, default='')
    
    # Timestamp from when the state snapshot was taken
    state_timestamp = models.DateTimeField('state timestamp')
    
    name = models.CharField(max_length=100, default='')
    where = models.CharField(max_length=100, default='')
    
    # Fields that are likely of greatest interest
    mode = models.CharField(max_length=100)
    fan = models.CharField(max_length=100)
    
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
    
    def __str__(self):
        return 'Device State at %s' % (str(self.state_timestamp))
    '''
     print '            Mode     : %s' % device.mode
        print '            Fan      : %s' % device.fan
        print '            Temp     : %0.1fC' % device.temperature
        print '            Humidity : %0.1f%%' % device.humidity
        print '            Target   : %0.1fC' % device.target
        print '            Away Heat: %0.1fC' % device.away_temperature[0]
        print '            Away Cool: %0.1fC' % device.away_temperature[1]

        print '            hvac_ac_state         : %s' % device.hvac_ac_state
        print '            hvac_cool_x2_state    : %s' % device.hvac_cool_x2_state
        print '            hvac_heater_state     : %s' % device.hvac_heater_state
        print '            hvac_aux_heater_state : %s' % device.hvac_aux_heater_state
        print '            hvac_heat_x2_state    : %s' % device.hvac_heat_x2_state
        print '            hvac_heat_x3_state    : %s' % device.hvac_heat_x3_state
        print '            hvac_alt_heat_state   : %s' % device.hvac_alt_heat_state
        print '            hvac_alt_heat_x2_state: %s' % device.hvac_alt_heat_x2_state
        print '            hvac_emer_heat_state  : %s' % device.hvac_emer_heat_state

        print '            online                : %s' % device.online
        print '            last_ip               : %s' % device.last_ip
        print '            local_ip              : %s' % device.local_ip
        print '            last_connection       : %s' % device.last_connection

        print '            error_code            : %s' % device.error_code
        print '            battery_level         : %s' % device.battery_level
    '''