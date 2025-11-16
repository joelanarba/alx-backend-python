#!/usr/bin/env python3
"""Unit tests for utils.access_nested_map, get_json, and memoize."""
import sys
import os
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized

# Add parent folder to path
sys.path.insert(0, os.path.abspath(".."))

# Import after path modification (with noqa to suppress E402)
from utils import access_nested_map, get_json, memoize  # noqa: E402


class TestAccessNestedMap(unittest.TestCase):
    """Test class for utils.access_nested_map."""
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test that access_nested_map returns the expected result."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b")
    ])
    def test_access_nested_map_exception(self, nested_map, path, missing_key):
        """Test that access_nested_map raises KeyError for missing keys."""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), f"'{missing_key}'")


class TestGetJson(unittest.TestCase):
    """Test class for utils.get_json."""
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(self, test_url, test_payload):
        """Test that get_json returns the expected payload with a mocked
        requests.get method."""
        with patch("utils.requests.get") as mock_get:
            mock_get.return_value = Mock()
            mock_get.return_value.json.return_value = test_payload
            result = get_json(test_url)
            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Test class for utils.memoize decorator."""
    def test_memoize(self):
        """Test that a memoized property calls the method only once."""
        class TestClass:
            """Test class with a method and a memoized property."""
            def a_method(self):
                """Return 42."""
                return 42

            @memoize
            def a_property(self):
                """A memoized property that calls a_method once and
                caches it."""
                return self.a_method()

        test_obj = TestClass()
        with patch.object(
            TestClass, "a_method", return_value=42
        ) as mock_method:
            result1 = test_obj.a_property
            result2 = test_obj.a_property
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()