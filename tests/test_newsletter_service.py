
"""Unit tests for the NewsletterService class."""

import unittest

from blog.author import Author
from blog.newsletter_service import NewsletterService
from blog.publisher import Publisher
from blog.subscriber import Subscriber


class TestNewsletterService(unittest.TestCase):
    """Test newsletters for newly registered authors."""

    def test_no_newsletter_before_three_authors(self):
        # given
        blog = Publisher()
        subscriber = Subscriber("Anna", tags=["Python"])
        blog.subscribe(subscriber)
        newsletter = NewsletterService(blog)

        # when
        blog.register_author(Author("John"))
        blog.register_author(Author("Maria"))

        # then
        self.assertFalse(subscriber.notifications)
        self.assertFalse(newsletter.newsletters_sent)

    def test_newsletter_sent_after_three_authors(self):
        # given
        blog = Publisher()
        anna = Subscriber("Anna", tags=["Python"])
        peter = Subscriber("Peter", tags=["Arduino"])
        blog.subscribe(anna)
        blog.subscribe(peter)
        newsletter = NewsletterService(blog)

        # when
        blog.register_author(Author("John"))
        blog.register_author(Author("Maria"))
        blog.register_author(Author("Alex"))

        # then
        self.assertEqual(len(newsletter.newsletters_sent), 1)
        self.assertIn("John", anna.notifications[0])
        self.assertIn("Maria", anna.notifications[0])
        self.assertIn("Alex", peter.notifications[0])
        self.assertEqual(anna.notifications, peter.notifications)

    def test_newsletter_counter_resets_after_sending(self):
        # given
        blog = Publisher()
        newsletter = NewsletterService(blog)

        # when
        for name in ["John", "Maria", "Alex", "David", "Emma"]:
            blog.register_author(Author(name))

        # then
        self.assertEqual(len(newsletter.newsletters_sent), 1)
        self.assertEqual(len(newsletter.new_authors), 2)

        # when
        blog.register_author(Author("Sophia"))

        # then
        self.assertEqual(len(newsletter.newsletters_sent), 2)
        self.assertFalse(newsletter.new_authors)


if __name__ == "__main__":
    unittest.main()
