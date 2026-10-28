
"""Unit tests for the Article class."""

import unittest

from blog.article import Article
from blog.author import Author


class TestArticle(unittest.TestCase):
    """Test article creation."""

    def test_article_has_author(self):
        # given
        author = Author("John")

        # when
        article = Article(
            "Learning Python",
            ["Python"],
            "Python basics",
            author
        )

        # then
        self.assertIs(article.author, author)


if __name__ == "__main__":
    unittest.main()
