import os, sys
import django
# Absolute path to my project where resource models are located
sys.path.append('C:\\Users\\krishnan\\reach_out_backend')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reach_out_backend.settings")
django.setup()
from django.conf import settings
from django.utils import timezone
if(settings.BASE_DIR not in sys.path): sys.path.append(settings.BASE_DIR)

from auth2.models import Profile
from staff.models import Constraint
from constants import ACTIVE_USER_TIMEOUT, RECENTLY_ACTIVE_USER_TIMEOUT
# Create constraint hourly_active_users = 3 : 12:00 || hourly_recently_active_users = 10 : 12:00 
# 4 - Active, 10 - Recently Active
# Create constraint hourly_active_users = 2 : 1:00 || hourly_recently_active_users = 5 : 1:00 

try:
    active_timeout = timezone.now() - timezone.timedelta(seconds=ACTIVE_USER_TIMEOUT)
    active_profiles = Profile.objects.filter(last_seen__gte=active_timeout)

    recently_active_timeout = timezone.now() - timezone.timedelta(seconds=RECENTLY_ACTIVE_USER_TIMEOUT)
    recently_active_profiles = Profile.objects.filter(last_seen__gte=recently_active_timeout)

    # Store if non-zero trail is detected
    if(Constraint.objects.filter(family='active_users').first()['value'] != 0 or Constraint.objects.filter(family='recently_active_users').first()['value']!=0 or active_profiles.count() != 0 or recently_active_profiles.count() != 0):
        Constraint.objects.create(family='active_users', handle={'value': active_profiles.count()})
        Constraint.objects.create(family='recently_active_users', handle={'value': recently_active_profiles.count()})
except Exception as e:
    import syslog
    syslog(syslog.LOG_WARNING, f"[D-Exception]:{e}")

