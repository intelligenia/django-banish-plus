import requests
from django.core.cache import cache
from celery import task
from django.conf import settings
from .models import Banishment
from celery.task import periodic_task

# Una vez al mes, limpiamos lista negra.
@periodic_task(run_every=crontab(day_of_month=1))
def clean_ip_blacklist():
    Banishment.objects.all().delete()

# Cada 5 minutos.
@periodic_task(run_every=crontab(minute='*/5'))
def update_ip_list():
    """ Background task to update the tor IP list.
    This is periodically configured to be run every 24 h.
    Results should be stord for longer period of time.
    """
    # Updating TOR exit node list from  CSV_URL
    TOR_CACHE_KEY = getattr(settings, 'TOR_CACHE_KEY')
    ips = fetch_tor_ip_list()
    cache.set(TOR_CACHE_KEY, ips, 3600*24*3)


def fetch_tor_ip_list():
    """ Stores Tor IP list to memcached
    :return: Set of IP addresses as string
    """
    TOR_IPS_DATABASE = getattr(settings, 'TOR_IPS_DATABASE')
    r = requests.get(TOR_IPS_DATABASE)
    results = []

    for row in r.content.split("\n"):
        row = row.strip()
        if not row:
            continue
        #print row
        results.append(row)

    return frozenset(results)
