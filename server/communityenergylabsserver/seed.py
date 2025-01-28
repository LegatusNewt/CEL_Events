from communityenergylabsserver.models.EventSchema import EventSchema, Event, save_events_data, RepeatTypes

# Seed EventSchema data into json file
def seed_events(file="server/data/data.json"):
    event_dicts = [
        {"id": 1, "name": "Test Event", "start_time": "2025-01-01T00:00:00", "end_time": "2025-01-01T06:00:00"},
        {"id": 2, "name": "Test Event 2", "start_time": "2025-01-02T12:00:00", "end_time": "2025-01-02T18:00:00" },
        {"id": 3, "name": "Test Event 3", "start_time": "2025-01-03T00:00:00", "end_time": "2025-01-03T06:00:00", "repeats": True, "repeat_types": [{ "type": RepeatTypes.WEEKLY.value, "num": 2}]},
        {"id": 4, "name": "Test Event 4", "start_time": "2025-01-04T00:00:00", "end_time": "2025-01-04T06:00:00", "repeats": True, "repeat_types": [{ "type": RepeatTypes.DAY_OF_WEEK.value, "num": 3}, { "type": RepeatTypes.DAY_OF_WEEK.value, "num": 4 }]},
    ]
    # Loads all data into EventSchema and returns list of Event objects
    event_schema = EventSchema(many=True)
    events = event_schema.load(event_dicts, many=True)
    
    # Write all data to file
    save_events_data(events, "server/data/data.json")

def seed_test_events(file="server/data/test_data.json"):
    seed_events(file)

# Run the seed function if this is main
if __name__ == "__main__":
    seed_events()