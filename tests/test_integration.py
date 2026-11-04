
"""Integration tests for the blog application."""

import unittest

from blog.analytics_service import AnalyticsService
from blog.article import Article
from blog.author import Author
from blog.event_bus import EventBus
from blog.newsletter_service import NewsletterService
from blog.publisher import Publisher
from blog.subscriber import Subscriber


class TestBlogIntegration(unittest.TestCase):
    """Test the collaboration of blog components."""

    def test_complete_blog_workflow(self):
        # given
        bus = EventBus()
        blog = Publisher(bus)
        analytics = AnalyticsService(bus)
        NewsletterService(blog)

        anna = Subscriber("Anna", tags=["Python"])
        blog.subscribe(anna)

        john = Author("John")
        maria = Author("Maria")
        alex = Author("Alex")

        # when
        blog.register_author(john)
        blog.register_author(maria)
        blog.register_author(alex)

        # then
        self.assertEqual(analytics.authors_registered, 3)
        self.assertEqual(len(anna.notifications), 1)
        self.assertIn("John", anna.notifications[0])

        # when
        anna.follow_author(john)

        article = Article(
            "Arduino Basics",
            ["Arduino"],
            "Learning Arduino",
            john
        )
        blog.publish(article)

        # then
        self.assertEqual(analytics.articles_published, 1)
        self.assertIn("Arduino Basics", anna.notifications)
        self.assertIn(article, blog.articles)


if __name__ == "__main__":
    unittest.main()
