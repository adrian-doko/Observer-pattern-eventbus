
"""Unit tests for the AnalyticsService class."""

import unittest

from blog.analytics_service import AnalyticsService
from blog.article import Article
from blog.author import Author
from blog.exceptions import MissingArticleTagsError
from blog.publisher import Publisher
from blog.subscriber import Subscriber


class TestAnalyticsService(unittest.TestCase):
    """Test blog analytics through events."""

    def test_author_registration_is_counted(self):
        # given
        blog = Publisher()
        analytics = AnalyticsService(blog.bus)

        # when
        blog.register_author(Author("John"))
        blog.register_author(Author("Maria"))

        # then
        self.assertEqual(analytics.authors_registered, 2)

    def test_subscriber_registration_is_counted(self):
        # given
        blog = Publisher()
        analytics = AnalyticsService(blog.bus)
        subscriber = Subscriber("Anna", tags=["Python"])

        # when
        blog.subscribe(subscriber)

        # then
        self.assertEqual(analytics.subscribers_registered, 1)

    def test_unsubscription_is_counted(self):
        # given
        blog = Publisher()
        analytics = AnalyticsService(blog.bus)
        subscriber = Subscriber("Anna", tags=["Python"])
        blog.subscribe(subscriber)

        # when
        blog.unsubscribe(subscriber)

        # then
        self.assertEqual(analytics.subscribers_unsubscribed, 1)

    def test_published_articles_are_counted(self):
        # given
        blog = Publisher()
        analytics = AnalyticsService(blog.bus)
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
        self.assertEqual(analytics.articles_published, 1)

    def test_duplicate_author_is_not_counted_twice(self):
        # given
        blog = Publisher()
        analytics = AnalyticsService(blog.bus)
        john = Author("John")

        # when
        blog.register_author(john)
        blog.register_author(john)

        # then
        self.assertEqual(analytics.authors_registered, 1)

    def test_rejected_article_is_not_counted(self):
        # given
        blog = Publisher()
        analytics = AnalyticsService(blog.bus)
        author = Author("John")
        article = Article(
            "General News",
            [],
            "An article without tags",
            author
        )

        # when / then
        with self.assertRaises(MissingArticleTagsError):
            blog.publish(article)

        self.assertEqual(analytics.articles_published, 0)


if __name__ == "__main__":
    unittest.main()
