from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
    )

    friendly_name = models.CharField(max_length=40, default='Friend')

    # Required when a user is requesting to pair
    nest_oauth_state = models.CharField(max_length=40, default='', null=True)
    nest_oauth_token = models.CharField(max_length=256, default='', null=True)  # Tokens are 146 chars today

    def __str__(self):
        return '%s (%s)' % (self.friendly_name, self.user.username)


class Device(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='devices')

    name = models.CharField(max_length=256, default='Unknown Thermostat')
    device_id = models.CharField(max_length=40)

    def __str__(self):
        return '%s''s device: %s' % (self.user_profile.friendly_name, self.name)


class DeviceState(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='states')

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

    hvac_state = models.CharField(max_length=100, default='unknown')

    online = models.BooleanField()
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
