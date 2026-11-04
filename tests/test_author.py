
"""Unit tests for the Author class."""

import unittest

from blog.author import Author


class TestAuthor(unittest.TestCase):
    """Test author creation."""

    def test_author_has_name(self):
        # given
        name = "John"

        # when
        author = Author(name)

        # then
        self.assertEqual(author.name, "John")


if __name__ == "__main__":
    unittest.main()
