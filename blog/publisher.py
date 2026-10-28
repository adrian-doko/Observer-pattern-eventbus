
"""Manage blog publishing and subscriptions."""

from .event_bus import EventBus
from .exceptions import MissingArticleTagsError


class Publisher:
    """Publish articles and manage subscriptions."""

    def __init__(self):
        self.articles = []
        self.subscribers = []
        self.authors = []
        self.bus = EventBus()

    def subscribe(self, subscriber):
        """Register a subscriber and emit an event."""
        if subscriber not in self.subscribers:
            self.subscribers.append(subscriber)
            self.bus.add("article_published", subscriber.notify)
            self.bus.emit("subscriber_registered", subscriber)

    def unsubscribe(self, subscriber):
        """Remove a subscriber and emit an event."""
        if subscriber in self.subscribers:
            self.subscribers.remove(subscriber)
            self.bus.remove("article_published", subscriber.notify)
            self.bus.emit("subscriber_unsubscribed", subscriber)

    def register_author(self, author):
        """Register a new author and emit an event."""
        if author not in self.authors:
            self.authors.append(author)
            self.bus.emit("author_registered", author)

    def publish(self, article):
        """Publish an article only if it has tags."""
        if not article.tags:
            raise MissingArticleTagsError(
                "An article must have at least one tag."
            )

        self.articles.append(article)
        self.bus.emit("article_published", article)
