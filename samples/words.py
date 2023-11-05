from typing import List
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class Event:
    title: str
    start: datetime
    end: datetime

def availabilities(events: List[Event], start: datetime, end: datetime, duration: timedelta) -> List[datetime]:
    """Given a list of booked 'events', a 'start' and an 'end' datetime, we want to return a list of possible start times for a new event with a given duration.
    
    Args:
        events: A list of 'Event's, denoting currently booked events.
        start: The earliest datetime we want the new event to start at.
        end: The latest datetime we want the new event to end at.
        duration: The duration of the new event we want to book.
    
    Returns:
        A list of possible datetimes for the new event. The new event must not overlap with any of the currently booked 'Event's, and its start and end dates must be within "start" and "end".
    """
    available_slots = []
    events = sorted(events, key=lambda x: x.start)
    
    current_start = start
    
    for event in events:
        if current_start + duration <= event.start:
            available_slots.append(current_start)
            current_start = event.end
        else:
            current_start = max(current_start, event.end)
    
    if current_start + duration <= end:
        available_slots.append(current_start)
    
    return available_slots

events = [
    Event("meeting1", datetime(2022, 12, 22, 8, 30), datetime(2022, 12, 22, 9, 30)),
    Event("meeting2", datetime(2022, 12, 22, 10, 30), datetime(2022, 12, 22, 11, 0)),
    Event("meeting3", datetime(2022, 12, 22, 13, 30), datetime(2022, 12, 22, 14, 0)),
    Event("meeting4", datetime(2022, 12, 22, 15, 00), datetime(2022, 12, 22, 16, 0))
]

# Test the function
slots = availabilities(events, datetime(2022, 12, 22, 9, 0), datetime(2022, 12, 22, 17, 0), timedelta(hours=1))
print(slots)

