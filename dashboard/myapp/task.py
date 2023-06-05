from django.core.cache import cache
from django.utils import timezone
from background_task import background

@background(schedule=3600)  # Runs every hour
def clear_cache():
    cache.clear()

@background(schedule=86400, queue='clear_cache_queue')  # Runs once a day at 2:00 AM
def clear_cache_daily():
    if timezone.now().hour == 2:
        clear_cache()
