
"""Article notification system using the Observer pattern."""


class MissingArticleTagsError(Exception):
    """Raised when an article has no tags."""

    pass


class Author:
    """Represent an author registered on the blog."""

    def __init__(self, name):
        self.name = name


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
    """Represent an article with a title, tags, body and author."""

    def __init__(self, title, tags, body, author):
        self.title = title
        self.tags = tags
        self.body = body
        self.author = author


class Subscriber:
    """Receive notifications for matching authors or topics."""

    def __init__(self, name, tags=None, authors=None):
        self.name = name
        self.tags = set(tags or [])
        self.authors = set(authors or [])
        self.notifications = []

    def notify(self, article):
        """Store a notification if author or tags match."""
        matches_tags = bool(self.tags.intersection(article.tags))
        matches_author = article.author in self.authors

        if matches_tags or matches_author:
            self.notifications.append(article.title)

    def follow_author(self, author):
        """Follow a new author."""
        self.authors.add(author)


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


class NewsletterService:
    """Send newsletters after a threshold of new authors."""

    def __init__(self, publisher, threshold=3):
        self.publisher = publisher
        self.threshold = threshold
        self.new_authors = []
        self.newsletters_sent = []

        publisher.bus.add(
            "author_registered",
            self.on_author_registered
        )

    def on_author_registered(self, author):
        """Collect authors and send a newsletter when ready."""
        self.new_authors.append(author)

        if len(self.new_authors) >= self.threshold:
            self.send_newsletter()
            self.new_authors.clear()

    def send_newsletter(self):
        """Notify subscribers about recently registered authors."""
        author_names = [author.name for author in self.new_authors]
        message = (
            "New authors: " + ", ".join(author_names)
            + ". You might be interested!"
        )

        for subscriber in self.publisher.subscribers:
            subscriber.notifications.append(message)

        self.newsletters_sent.append(message)


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
