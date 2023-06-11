import os, sys
import django
# Absolute path to my project where resource models are located
sys.path.append('C:\\Users\\krishnan\\reach_out_backend')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reach_out_backend.settings")
django.setup()
from django.conf import settings
from django.utils import timezone
if(settings.BASE_DIR not in sys.path): sys.path.append(settings.BASE_DIR)
from staff.models import Constraint
from constants import CONSTRAINT_CLEANUP_THRESHOLDS_MONTHS

try:

    active_threshold = timezone.now() - timezone.timedelta(weeks=CONSTRAINT_CLEANUP_THRESHOLDS_MONTHS['ACTIVE_USER'])
    recently_active_threshold = timezone.now() - timezone.timedelta(seconds=CONSTRAINT_CLEANUP_THRESHOLDS_MONTHS['RECENTLY_ACTIVE_USER'])

    stale = Constraint.objects.filter(family='active_users', added_at__lt=active_threshold)
    stale._raw_delete(stale.db)

    stale = Constraint.objects.filter(family='recently_active_threshold', added_at__lt=recently_active_threshold)
    stale._raw_delete(stale.db)

except Exception as e:
    import syslog
    syslog(syslog.LOG_WARNING, f"[D-Exception]:{e}")
    