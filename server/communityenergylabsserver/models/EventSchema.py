from typing import List
from marshmallow import Schema, fields, ValidationError, validates, validates_schema, pre_load, post_load
from datetime import datetime
from dateutil import parser, rrule, relativedelta
from enum import Enum
from copy import deepcopy
import json

class Event:
    id: int
    name: str
    description: str
    start_time: datetime
    end_time: datetime
    repeats: bool
    repeat_types: dict

    def __init__(self, id, name, start_time, end_time, repeats=False, repeat_types={}, description=None):
        self.id = id
        self.name = name
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
        self.repeats = repeats
        self.repeat_types = repeat_types

    # Update Event data
    def update(self, **kwargs):
        if "name" in kwargs:
            self.name = kwargs["name"]
        if "description" in kwargs:
            self.description = kwargs["description"]
        if "start_time" in kwargs:
            self.start_time = kwargs["start_time"]
        if "end_time" in kwargs:
            self.end_time = kwargs["end_time"]
        if "repeats" in kwargs:
            self.repeats = kwargs["repeats"]
        if "repeat_types" in kwargs:
            self.repeat_types = kwargs["repeat_types"]

    # Based on repeat_interval, generate repeat_dates within given window
    def produce_repeat_events(self, start_window, end_window):
        repeat_dates = []
        for item in self.repeat_types:
            # Get repeat type and value
            if item["type"] == RepeatTypes.DAILY:                
                # Repeat every day or every x days ex starting from start_time
                repeat_rule = rrule.rrule(rrule.DAILY, bysetpos=self.start_time.day ,dtstart=start_window, until=end_window, interval=item["num"])
            elif item["type"] == RepeatTypes.WEEKLY.value:
                # Repeat every week on the same day of the week or every x weeks ex. { "weekly": 2 } would repeat every 2 weeks
                repeat_rule = rrule.rrule(rrule.WEEKLY, byweekday=self.start_time.weekday(), dtstart=start_window, until=end_window, interval=item["num"])                
            elif item["type"] == RepeatTypes.WHICH_WEEK.value:
                # Repeat every month on the same week of the month ex. { "whichweek": 2 } would repeat every 2nd week of the month on the same day of the week
                repeat_rule = rrule.rrule(rrule.MONTHLY, byweekno=item["num"], byweekday=start_window.weekday(), dtstart=start_window, until=end_window)
            elif item["type"] == RepeatTypes.MONTHLY.value:
                # Repeat every month on the same day of the month ex. { "monthly": 2 } would repeat every 2nd day of the month
                repeat_rule = rrule.rrule(rrule.MONTHLY, bymonthday=item["num"], dtstart=start_window, until=end_window)
            elif item["type"] == RepeatTypes.DAY_OF_WEEK.value:
                # Repeat every week on specific days of week ex. { "dayofweek": [0, 2, 4] } would repeat every Monday, Wednesday, Friday
                repeat_rule = rrule.rrule(rrule.WEEKLY, byweekday=item["num"], dtstart=start_window, until=end_window)
            
            # Add new repeat dates to list
            repeat_dates.extend(repeat_rule)

        repeat_events = []
        # Format event start time and end time based on repeat dates
        for date in repeat_dates:
            # If the window start date is before the event start date only send back events that are after the event start
            if date > self.start_time:
                new_event = deepcopy(self)
                # Update start and end time with new date
                # This won't work on events that have cross two days might need special logic for that in the future
                new_event.start_time = new_event.start_time.replace(year=date.year, month=date.month, day=date.day) # Keep timestamps
                new_event.end_time = new_event.end_time.replace(year=date.year, month=date.month, day=date.day) # Keep timestamps
                repeat_events.append(new_event)
        return repeat_events    

class RepeatTypes(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    WHICH_WEEK = "whichweek"
    DAY_OF_WEEK = "dayofweek"
    MONTHLY = "monthly"

class EventSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(required=True)
    repeats = fields.Bool(allow_none=True)
    repeat_types = fields.List(fields.Dict, allow_none=True)

    def update(self, instance, validated_data):
        instance.update(**validated_data)
        return instance

    # Write to class
    @post_load
    def write_to_class(self, data, **kwargs):
        return Event(**data)

    @validates_schema
    def proper_dates(self, data, **kwargs):
        if data["start_time"] > data["end_time"]:
            raise ValidationError("Start date must be before end date")
        return data
    
    def load_all_data(self, file):
        with open(file, 'r') as json_file:
            data = json.load(json_file)
            try:
                events = EventSchema(many=True).load(data)
                return events
            except ValidationError as err:
                return json.dumps(err.messages), 400               

# TODO: Improvement:
#  Implement save as we go -> sync events data to file on every change rather than a full file rewrite

# Save all Event data to file
def save_events_data(events: List[Event], file):
    # Write all data to file
    with open(file, 'w') as json_file:
        try:
            # Serialize using Marshmallow EventSchema
            events_schemas = EventSchema(many=True).dump(events)
            json_string = json.dumps(events_schemas)
            json_file.write(json_string)
        except Exception as e:
            return e, 400
        return "Data saved", 200

# Loads all data into EventSchema and returns list of Event objects
def load_events_data(file):
    event_schema = EventSchema(many=True)
    with open(file, 'r') as json_file:
        data = json.load(json_file)
        try:
            events = event_schema.load(data, partial=True)
            return events
        except ValidationError as err:
            return json.dumps(err.messages), 400