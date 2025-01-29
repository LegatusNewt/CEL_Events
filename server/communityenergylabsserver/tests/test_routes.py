from communityenergylabsserver.flaskr import create_app
from communityenergylabsserver.models.EventSchema import EventSchema, Event, RepeatTypes
from datetime import datetime
import json

def test_index(client):
    response = client.get("/")
    # Test HTML response, looking for div with id="app"
    decoded = response.data.decode("utf-8")
    assert decoded.index('<div id="app">') != -1

def test_hello(client):
    # Test /hello route
    response = client.get("/hello")
    assert response.data == b"Hello, World!"

def test_events_get(client):
    response = client.get("/events")
    assert response.status_code == 200
    data = response.json
    assert len(data) == 4
    

# Test Posting overlapping events
def test_events_post_overlap(client):
    response = client.post("/events", json={"name": "Test Event", "start_time": "2025-01-10T00:00:00", "end_time": "2025-01-10T06:00:00"})
    _id = response.json['id']
    assert response.status_code == 200
    response = client.post("/events", json={"name": "Test Event", "start_time": "2025-01-10T00:00:00", "end_time": "2025-01-10T07:00:00"})
    assert response.status_code == 400

# Test posting a new event
def test_events_post(client):
    response = client.post("/events", json={"name": "Test Event", "start_time": "2025-01-15T00:00:00", "end_time": "2025-01-15T06:00:00"})
    assert response.status_code == 200
    assert response.json['id'] == 5

# Test updating an event
def test_events_update(client):
    response = client.post("/events", json={"name": "Test Event", "start_time": "2025-01-30T00:00:00", "end_time": "2025-01-30T06:00:00"})
    assert response.status_code == 200
    id = response.json['id']

    response = client.put(f"/events/{id}", json={"name": "Updated Event"})
    assert response.status_code == 200
    assert response.json['name'] == "Updated Event"


# Test schedule endpoint returns correct number of events
def test_schedule(client):
    response = client.get("/events/schedule?start_date=2025-01-01T00:00:00&end_date=2025-02-01T00:00:00")
    assert response.status_code == 200
    assert len(response.json) == 16

# TODO: Test all the other options for repeating events
def test_repeat_dates_function():
    # Generate Event with Monday and Tuesday repeats
    event = EventSchema().load({"id": 1, "name": "Test Event", "start_time": "2025-01-01T00:00:00", "end_time": "2025-01-01T06:00:00", "repeats": True, "repeat_types": [{"type": RepeatTypes.DAY_OF_WEEK.value, "num": 0}, {"type": RepeatTypes.DAY_OF_WEEK.value, "num": 1}]})
    # Generate repeat dates
    repeat_dates = event.produce_repeat_events(datetime.fromisoformat("2025-01-01T00:00:00"), datetime.fromisoformat("2025-01-31T00:00:00"))
    # Assert that there are 8 repeat dates
    assert len(repeat_dates) == 8
