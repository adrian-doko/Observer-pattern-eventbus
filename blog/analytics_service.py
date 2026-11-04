
"""Track blog activity using EventBus."""


class AnalyticsService:
    """Track blog activity through events."""

    def __init__(self, bus):
        self.authors_registered = 0
        self.subscribers_registered = 0
        self.subscribers_unsubscribed = 0
        self.articles_published = 0

        bus.add("author_registered", self.on_author_registered)
        bus.add("subscriber_registered", self.on_subscriber_registered)
        bus.add("subscriber_unsubscribed", self.on_subscriber_unsubscribed)
        bus.add("article_published", self.on_article_published)

    def on_author_registered(self, author):
        """Count newly registered authors."""
        self.authors_registered += 1

    def on_subscriber_registered(self, subscriber):
        """Count new subscriptions."""
        self.subscribers_registered += 1

    def on_subscriber_unsubscribed(self, subscriber):
        """Count removed subscriptions."""
        self.subscribers_unsubscribed += 1

    def on_article_published(self, article):
        """Count published articles."""
        self.articles_published += 1
