import os, sys
import django
# Absolute path to my project where resource models are located
sys.path.append('C:\\Users\\krishnan\\reach_out_backend')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reach_out_backend.settings")
django.setup()
from django.conf import settings
from django.utils import timezone
if(settings.BASE_DIR not in sys.path): sys.path.append(settings.BASE_DIR)

from auth2.models import ProfilePoint
from staff.models import Constraint
from constants import ACTIVE_USER_TIMEOUT, RECENTLY_ACTIVE_USER_TIMEOUT
from global_utils.functions import parse_data_from_ips

ip_to_points:dict = {}
#Ex.. {'12.23.43.33': [<ProfilePoint:krishnan>, <ProfilePoint:omkar>], ...}
# Additionally GenericIpField can't be null as pre-defined in models, so skipping null_check
try:
    profile_points = ProfilePoint.objects.all()

    for profile_point in list(profile_points):
        if(ip_to_points.get(profile_point.ip, False)):
            ip_to_points[profile_point.ip].append(profile_point)
        else:
            ip_to_points[profile_point.ip] = [profile_point]

    # I am replicating this array data to dictionary because suppose we got request / response like this order,
    '''
    Request: <ProfilePoint:1.2.3.4>, <ProfilePoint:1.2.3.4>
    Response: {1.2.3.4: Ahmedabad} <- filtered + non-duplicated + have to check and iterate 
    '''

    response:dict = parse_data_from_ips(profile_points.keys(), op_label='city')
    # Format: {'1.2.3.4/city': 'Ahmedabad'}
    if(type(response) != dict):
        import syslog
        syslog(syslog.LOG_WARNING, f"[D-Exception]:{e}")

    for ip_with_noise, city in response.items():
        pure_ip = ip_with_noise.split('/')[0]
        for point in ip_to_points[pure_ip]:
            point.city = city
            point.save()
except Exception as e:
    import syslog
    syslog(syslog.LOG_WARNING, f"[D-Exception]:{e}")




