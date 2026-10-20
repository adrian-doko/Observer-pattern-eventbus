
"""Unit tests for the Observer Pattern project."""

import unittest

from event import Article, EventBus, Publisher, Subscriber


class TestPublisher(unittest.TestCase):
    """Test publisher and subscriber behavior."""

    def test_subscriber_receives_notification(self):
        # given
        blog = Publisher()
        adrian = Subscriber("Adrian", ["Python"])
        blog.subscribe(adrian)

        article = Article(
            "Learning Python",
            ["Python"],
            "Python basics"
        )

        # when
        blog.publish(article)

        # then
        self.assertTrue(
            "Learning Python" in adrian.notifications
        )

    def test_article_is_stored(self):
        # given
        blog = Publisher()
        article = Article(
            "Arduino Sensors",
            ["Arduino"],
            "Learning about Arduino sensors"
        )

        # when
        blog.publish(article)

        # then
        self.assertTrue(article in blog.articles)

    def test_unsubscribed_user_receives_no_notification(self):
        # given
        blog = Publisher()
        adrian = Subscriber("Adrian", ["Python"])
        blog.subscribe(adrian)

        article = Article(
            "Learning Python",
            ["Python"],
            "Python basics"
        )

        # when
        blog.unsubscribe(adrian)
        blog.publish(article)

        # then
        self.assertFalse(adrian.notifications)
        self.assertFalse(adrian in blog.subscribers)

    def test_resubscribe_receives_notification(self):
        # given
        blog = Publisher()
        adrian = Subscriber("Adrian", ["Python"])

        blog.subscribe(adrian)
        blog.unsubscribe(adrian)

        article = Article(
            "Learning Python",
            ["Python"],
            "Python basics"
        )

        # when
        blog.subscribe(adrian)
        blog.publish(article)

        # then
        self.assertTrue(adrian in blog.subscribers)
        self.assertEqual(
            adrian.notifications,
            ["Learning Python"]
        )

    def test_multiple_matching_tags_send_one_notification(self):
        # given
        blog = Publisher()
        adrian = Subscriber("Adrian", ["Python", "Arduino"])
        blog.subscribe(adrian)

        article = Article(
            "Python for Arduino",
            ["Python", "Arduino"],
            "Using Python with Arduino"
        )

        # when
        blog.publish(article)

        # then
        self.assertEqual(
            adrian.notifications,
            ["Python for Arduino"]
        )

    def test_article_without_tags_sends_no_notification(self):
        # given
        blog = Publisher()
        adrian = Subscriber("Adrian", ["Python"])
        blog.subscribe(adrian)

        article = Article(
            "General News",
            [],
            "This article has no tags."
        )

        # when
        blog.publish(article)

        # then
        self.assertFalse(adrian.notifications)
        self.assertTrue(article in blog.articles)


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
        self.assertTrue("Hello" in received)

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
