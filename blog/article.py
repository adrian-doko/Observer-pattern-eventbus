
"""Define an article published on the blog."""


class Article:
    """Represent an article with a title, tags, body and author."""

    def __init__(self, title, tags, body, author):
        self.title = title
        self.tags = tags
        self.body = body
        self.author = author
