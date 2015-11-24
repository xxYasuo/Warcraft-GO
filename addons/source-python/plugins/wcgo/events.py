"""Contains the functionality for calling skills through SP events."""

# Source.Python
import events


class Event(events.Event):
    """Event decorator which stores the events to a set."""
    _instances = set()

    def __init__(self, *event_names):
        """Store the event names."""
        super().__init__(*event_names)
        _events.append(self)

    @classmethod 
    def unregister_all(cls):
        """Unregister the event callbacks."""
        for event in cls._instances:
            event._unload_instance()
