
"""Unit tests for the Publisher class."""

import unittest

from blog.article import Article
from blog.author import Author
from blog.exceptions import MissingArticleTagsError
from blog.publisher import Publisher
from blog.subscriber import Subscriber


class TestPublisher(unittest.TestCase):
    """Test publisher and subscriber behavior."""

    def test_article_is_stored(self):
        # given
        blog = Publisher()
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
        self.assertIn(article, blog.articles)

    def test_article_without_tags_is_rejected(self):
        # given
        blog = Publisher()
        author = Author("John")
        article = Article(
            "General News",
            [],
            "Article without tags",
            author
        )

        # when / then
        with self.assertRaises(MissingArticleTagsError):
            blog.publish(article)

        self.assertNotIn(article, blog.articles)

    def test_subscriber_receives_notification(self):
        # given
        blog = Publisher()
        author = Author("John")
        subscriber = Subscriber("Anna", tags=["Python"])
        blog.subscribe(subscriber)

        article = Article(
            "Learning Python",
            ["Python"],
            "Python basics",
            author
        )

        # when
        blog.publish(article)

        # then
        self.assertEqual(
            subscriber.notifications,
            ["Learning Python"]
        )

    def test_subscriber_receives_notification_by_author(self):
        # given
        blog = Publisher()
        author = Author("John")
        subscriber = Subscriber("Anna", authors=[author])
        blog.subscribe(subscriber)

        article = Article(
            "Learning Arduino",
            ["Arduino"],
            "Arduino basics",
            author
        )

        # when
        blog.publish(article)

        # then
        self.assertEqual(
            subscriber.notifications,
            ["Learning Arduino"]
        )

    def test_matching_author_and_topic_sends_one_notification(self):
        # given
        blog = Publisher()
        author = Author("John")
        subscriber = Subscriber(
            "Anna",
            tags=["Python"],
            authors=[author]
        )
        blog.subscribe(subscriber)

        article = Article(
            "Learning Python",
            ["Python"],
            "Python basics",
            author
        )

        # when
        blog.publish(article)

        # then
        self.assertEqual(
            subscriber.notifications,
            ["Learning Python"]
        )

    def test_unsubscribed_user_receives_no_notification(self):
        # given
        blog = Publisher()
        author = Author("John")
        subscriber = Subscriber("Anna", tags=["Python"])
        blog.subscribe(subscriber)

        article = Article(
            "Learning Python",
            ["Python"],
            "Python basics",
            author
        )

        # when
        blog.unsubscribe(subscriber)
        blog.publish(article)

        # then
        self.assertFalse(subscriber.notifications)
        self.assertNotIn(subscriber, blog.subscribers)

    def test_resubscribe_receives_notification(self):
        # given
        blog = Publisher()
        author = Author("John")
        subscriber = Subscriber("Anna", tags=["Python"])
        blog.subscribe(subscriber)
        blog.unsubscribe(subscriber)

        article = Article(
            "Learning Python",
            ["Python"],
            "Python basics",
            author
        )

        # when
        blog.subscribe(subscriber)
        blog.publish(article)

        # then
        self.assertEqual(
            subscriber.notifications,
            ["Learning Python"]
        )

    def test_multiple_matching_tags_send_one_notification(self):
        # given
        blog = Publisher()
        author = Author("John")
        subscriber = Subscriber(
            "Anna",
            tags=["Python", "Arduino"]
        )
        blog.subscribe(subscriber)

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
            subscriber.notifications,
            ["Python for Arduino"]
        )

    def test_subscriber_receives_notification_by_topic(self):
        # given
        blog = Publisher()
        author = Author("John")
        subscriber = Subscriber("Anna", tags=["Python"])
        blog.subscribe(subscriber)

        article = Article(
            "Python Basics",
            ["Python"],
            "Learning Python",
            author
        )

        # when
        blog.publish(article)

        # then
        self.assertEqual(
            subscriber.notifications,
            ["Python Basics"]
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
            "Arduino Basics",
            ["Arduino"],
            "Learning Arduino",
            john
        )

        # when
        blog.publish(article)

        # then
        self.assertFalse(subscriber.notifications)
        self.assertIn(article, blog.articles)

    def test_subscriber_can_follow_new_author(self):
        # given
        blog = Publisher()
        john = Author("John")
        subscriber = Subscriber("Anna", tags=["Python"])
        blog.subscribe(subscriber)

        article = Article(
            "Arduino Basics",
            ["Arduino"],
            "Learning Arduino",
            john
        )

        # when
        subscriber.follow_author(john)
        blog.publish(article)

        # then
        self.assertIn(john, subscriber.authors)
        self.assertEqual(
            subscriber.notifications,
            ["Arduino Basics"]
        )

    def test_author_registration(self):
        # given
        blog = Publisher()
        john = Author("John")

        # when
        blog.register_author(john)

        # then
        self.assertIn(john, blog.authors)

    def test_duplicate_author_registration(self):
        # given
        blog = Publisher()
        john = Author("John")

        # when
        blog.register_author(john)
        blog.register_author(john)

        # then
        self.assertEqual(blog.authors, [john])

    def test_author_registration_emits_event(self):
        # given
        blog = Publisher()
        john = Author("John")
        received = []

        def handler(author):
            received.append(author)

        blog.bus.add("author_registered", handler)

        # when
        blog.register_author(john)

        # then
        self.assertEqual(received, [john])


if __name__ == "__main__":
    unittest.main()
