"""Provides Event class for observer pattern events."""


class Event(list):
    """A simple Event class subclassing list."""

    def fire(self, sender, **event_args):
        """Fire an event with the provided arguments."""
        for observer in self:
            observer(sender, **event_args)

    def __iadd__(self, observer):
        """Add an observer to the event."""
        self.append(observer)
        return self

    def __isub__(self, observer):
        """Remove an observer from the event."""
        self.remove(observer)
        return self
