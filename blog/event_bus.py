
"""Manage events using the Observer pattern."""


class EventBus:
    """Manage event listeners and dispatch events."""

    def __init__(self):
        self.handlers = {}

    def add(self, event_name, handler):
        """Register a handler for an event."""
        handlers = self.handlers.setdefault(event_name, [])

        if handler not in handlers:
            handlers.append(handler)

    def remove(self, event_name, handler):
        """Remove a handler from an event."""
        handlers = self.handlers.get(event_name, [])

        if handler in handlers:
            handlers.remove(handler)

    def emit(self, event_name, data=None):
        """Call all handlers registered for an event."""
        for handler in list(self.handlers.get(event_name, [])):
            handler(data)
