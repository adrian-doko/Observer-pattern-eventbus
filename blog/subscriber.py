
"""Manage blog subscribers and their interests."""


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
