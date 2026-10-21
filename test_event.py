
"""Unit tests for the Observer Pattern project."""

import unittest

from event import (
    Article,
    Author,
    EventBus,
    MissingArticleTagsError,
    Publisher,
    Subscriber,
)


class TestAuthor(unittest.TestCase):
    """Test author creation."""

    def test_author_has_name(self):
        # given
        name = "John"

        # when
        author = Author(name)

        # then
        self.assertEqual(author.name, "John")


class TestArticle(unittest.TestCase):
    """Test article creation."""

    def test_article_has_author(self):
        # given
        author = Author("John")

        # when
        article = Article(
            "Learning Python",
            ["Python"],
            "Python basics",
            author
        )

        # then
        self.assertIs(article.author, author)


class TestPublisher(unittest.TestCase):
    """Test publisher and subscriber behavior."""

    def test_subscriber_receives_notification(self):
        # given
        blog = Publisher()
        adrian = Subscriber("Adrian", ["Python"])
        blog.subscribe(adrian)
        author = Author("John")

        article = Article(
            "Learning Python",
            ["Python"],
            "Python basics",
            author
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
        author = Author("John")
        article = Article(
            "Arduino Sensors",
            ["Arduino"],
            "Learning about Arduino sensors",
            author
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
        author = Author("John")

        article = Article(
            "Learning Python",
            ["Python"],
            "Python basics",
            author
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
        author = Author("John")

        article = Article(
            "Learning Python",
            ["Python"],
            "Python basics",
            author
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
        author = Author("John")

        article = Article(
            "Python for Arduino",
            ["Python", "Arduino"],
            "Using Python with Arduino",
            author
        )

        # when
        blog.publish(article)

        # then
        self.assertEqual(
            adrian.notifications,
            ["Python for Arduino"]
        )

    def test_article_without_tags_is_rejected(self):
        # given
        blog = Publisher()
        author = Author("John")
        article = Article(
            "General News",
            [],
            "This article has no tags.",
            author
        )

        # when / then
        with self.assertRaises(MissingArticleTagsError):
            blog.publish(article)

        self.assertFalse(article in blog.articles)

    def test_subscriber_receives_notification_by_author(self):
        # given
        blog = Publisher()
        john = Author("John")
        subscriber = Subscriber("Anna", authors=[john])
        blog.subscribe(subscriber)

        article = Article(
            "Learning Arduino",
            ["Arduino"],
            "Arduino basics",
            john
        )

        # when
        blog.publish(article)

        # then
        self.assertEqual(
            subscriber.notifications,
            ["Learning Arduino"]
        )

    def test_subscriber_receives_notification_by_topic(self):
        # given
        blog = Publisher()
        john = Author("John")
        subscriber = Subscriber("Anna", tags=["Python"])
        blog.subscribe(subscriber)

        article = Article(
            "Learning Python",
            ["Python"],
            "Python basics",
            john
        )

        # when
        blog.publish(article)

        # then
        self.assertEqual(
            subscriber.notifications,
            ["Learning Python"]
        )

    def test_matching_author_and_topic_sends_one_notification(self):
        # given
        blog = Publisher()
        john = Author("John")
        subscriber = Subscriber(
            "Anna",
            tags=["Python"],
            authors=[john]
        )
        blog.subscribe(subscriber)

        article = Article(
            "Learning Python",
            ["Python"],
            "Python basics",
            john
        )

        # when
        blog.publish(article)

        # then
        self.assertEqual(
            subscriber.notifications,
            ["Learning Python"]
        )

    def test_no_notification_when_author_and_topic_do_not_match(self):
        # given
        blog = Publisher()
        john = Author("John")
        maria = Author("Maria")

        subscriber = Subscriber(
            "Anna",
            tags=["Python"],
            authors=[maria]
        )
        blog.subscribe(subscriber)

        article = Article(
            "Learning Arduino",
            ["Arduino"],
            "Arduino basics",
            john
        )

        # when
        blog.publish(article)

        # then
        self.assertFalse(subscriber.notifications)
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
