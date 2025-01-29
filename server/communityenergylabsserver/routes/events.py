from flask import Blueprint, request, jsonify
from communityenergylabsserver.cache import cache
from communityenergylabsserver.models.EventSchema import EventSchema, Event, load_events_data, save_events_data
from datetime import datetime
import json

event_routes = Blueprint('event_routes', __name__)

@event_routes.route('/events', methods=['GET'])
def get_events():
    events = cache.get('events')

    # Convert to list to make use of Desrialize in Marshmallow
    events = list(events.values())
    return EventSchema().dumps(events, many=True)

@event_routes.route('/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    events = cache.get('events')
    res = EventSchema().dumps(events[event_id])
    return res

@event_routes.route('/events/schedule', methods=['GET'])
# Get all events between two dates
def get_schedule():
    start_date = datetime.fromisoformat(request.args.get('start_date'))
    end_date = datetime.fromisoformat(request.args.get('end_date'))
    events = cache.get('events')
    # Check for events between start and end date
    if not events:
        return jsonify("No events found")
    scheduled_events = [event for event in events.values() if event.start_time >= start_date and event.end_time <= end_date]

    # Check repeat events
    repeat_events = [event for event in events.values() if event.repeats]
    
    # For every repeat event get all event dates between start and end date
    for event in repeat_events:
        repeat_events = event.produce_repeat_events(start_date, end_date)
        # Extend the list of scheduled events with the same event on the new dates

        scheduled_events.extend(repeat_events)
    return EventSchema().dumps(scheduled_events, many=True)
    
    

# POST event data
@event_routes.route('/events', methods=['POST'])
def post_event():
    # Read request data
    body = request.json
    # Get all events from cache
    events = cache.get('events')
    # hacky autoincrement id, should be handled by database
    new_id = max(events.keys()) + 1

    # Form new Event class object from POST json
    body['id'] = new_id
    new_event = EventSchema().load(body)

    events.update({new_id: new_event})
    cache.set('events', events)
    # Return event ID as json
    return jsonify({"id": new_id})

@event_routes.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    # Deletes an Event from the cache
    events = cache.get('events')
    events.pop(event_id)
    cache.set('events', events)
    return f'Event {event_id} Deleted'

@event_routes.route('/events', methods=['PATCH'])
def save_cache():
    # This way the application can control when the cache is saved, ideally this would be done on every change
        # For testing purposes I wanted this as a route
    events = cache.get('events')
    save_events_data(list(events.values()), 'server/data/data.json')

    # TODO: Future Improvement tie each user session to cache file, so that only their data is saved
    return 'Data saved for user'

# Modify event data
@event_routes.route('/events/<int:event_id>', methods=['PUT'])
def put_event(event_id):
    # Read request data
    body = request.json
    # Get all events from cache
    events = cache.get('events')

    # Get the event to modify
    event = events[event_id]
    
    # Update the event with the new data
    schema_dict = EventSchema().dump(event)
    schema_dict.update(**body)

    # Form new Event class object from PUT json
    new_event = EventSchema().load(schema_dict)

    print(new_event)
    
    # Save the updated event back to the cache
    events[event_id] = new_event
    cache.set('events', events)

    # Return new event data
    return EventSchema().dumps(new_event)
