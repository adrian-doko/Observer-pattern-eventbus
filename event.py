
"""Article notification system using the Observer pattern."""


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


class Article:
    """Represent an article with a title, tags and body."""

    def __init__(self, title, tags, body):
        self.title = title
        self.tags = tags
        self.body = body


class Subscriber:
    """Receive notifications for matching article tags."""

    def __init__(self, name, tags):
        self.name = name
        self.tags = set(tags)
        self.notifications = []

    def notify(self, article):
        """Store a notification if article tags match."""
        if self.tags.intersection(article.tags):
            self.notifications.append(article.title)


class Publisher:
    """Publish articles and manage subscriptions."""

    def __init__(self):
        self.articles = []
        self.subscribers = []
        self.bus = EventBus()

    def subscribe(self, subscriber):
        """Register a subscriber for article events."""
        if subscriber not in self.subscribers:
            self.subscribers.append(subscriber)
            self.bus.add("article_published", subscriber.notify)

    def unsubscribe(self, subscriber):
        """Remove a subscriber from article events."""
        if subscriber in self.subscribers:
            self.subscribers.remove(subscriber)
            self.bus.remove("article_published", subscriber.notify)

    def publish(self, article):
        """Store an article and notify subscribers."""
        self.articles.append(article)
        self.bus.emit("article_published", article)
