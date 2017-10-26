import requests
from celery.schedules import crontab
from django.core.cache import cache
from celery import task
from django.conf import settings
from .models import Banishment
from celery.task import periodic_task


@app.task(bind=True)
def clean_ip_blacklist(self):
    Banishment.objects.all().delete()

# Cada 5 minutos.
@app.task(bind=True)
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
