from flask_caching import Cache
from communityenergylabsserver.models.EventSchema import load_events_data

# Initialize cache
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})

def preload_cache():
    events_list = load_events_data('server/data/data.json')

    #Convert to dict with ID as key
    events_dict = {event.id: event for event in events_list}
    cache.add('events', events_dict)