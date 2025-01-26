from flask import Blueprint

event_routes = Blueprint('event_routes', __name__)

@event_routes.route('/events')
def get_events():
    return 'Events Home'

@event_routes.route('/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    return f'Event {event_id}'

# POST event data
@event_routes.route('/events', methods=['POST'])
def post_event():
    # Return event ID
    return 'Event Created'

# Modify event data
@event_routes.route('/events/<int:event_id>', methods=['PUT'])
def put_event(event_id):
    return f'Event {event_id} Modified'

