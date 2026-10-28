
"""Unit tests for the EventBus class."""

import unittest

from blog.event_bus import EventBus


class TestEventBus(unittest.TestCase):
    """Test adding, removing and dispatching listeners."""

    def test_added_listener_receives_event(self):
        # given
        bus = EventBus()
        received = []

        def handler(data):
            received.append(data)

        bus.add("message", handler)

        # when
        bus.emit("message", "Hello")

        # then
        self.assertIn("Hello", received)

    def test_removed_listener_receives_no_event(self):
        # given
        bus = EventBus()
        received = []

        def handler(data):
            received.append(data)

        bus.add("message", handler)

        # when
        bus.remove("message", handler)
        bus.emit("message", "Hello")

        # then
        self.assertFalse(received)

    def test_duplicate_listener_is_called_once(self):
        # given
        bus = EventBus()
        received = []

        def handler(data):
            received.append(data)

        bus.add("message", handler)
        bus.add("message", handler)

        # when
        bus.emit("message", "Hello")

        # then
        self.assertEqual(len(received), 1)


if __name__ == "__main__":
    unittest.main()
