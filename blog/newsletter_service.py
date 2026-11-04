
"""Send newsletters about newly registered authors."""


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
