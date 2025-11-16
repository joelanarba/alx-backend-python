#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient."""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient methods."""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test GithubOrgClient.org returns correct value."""
        mock_get_json.return_value = {"login": org_name}
        client = GithubOrgClient(org_name)
        result = client.org
        mock_get_json.assert_called_once_with(
            "https://api.github.com/orgs/{}".format(org_name)
        )
        self.assertEqual(result, {"login": org_name})

    def test_public_repos_url(self):
        """Test GithubOrgClient._public_repos_url returns correct URL."""
        client = GithubOrgClient("google")
        payload = {"repos_url": "https://api.github.com/orgs/google/repos"}
        with patch.object(
            GithubOrgClient, "org", new_callable=Mock
        ) as mock_org:
            mock_org.return_value = payload
            result = client._public_repos_url
            self.assertEqual(
                result, "https://api.github.com/orgs/google/repos"
            )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos returns correct repo list."""
        payload = [{"name": "repo1"}, {"name": "repo2"}]
        mock_get_json.return_value = payload
        client = GithubOrgClient("google")
        with patch.object(
            GithubOrgClient, "_public_repos_url", new_callable=Mock
        ) as mock_url:
            mock_url.return_value = "mocked_url"
            result = client.public_repos()
            self.assertEqual(result, ["repo1", "repo2"])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with("mocked_url")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test GithubOrgClient.has_license returns True if license matches."""
        client = GithubOrgClient("google")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": {"repos_url": "https://api.github.com/orgs/google/repos"},
        "repos_payload": [
            {"name": "repo1", "license": {"key": "apache-2.0"}},
            {"name": "repo2", "license": {"key": "bsd-3-clause"}}
        ],
        "expected_repos": ["repo1", "repo2"],
        "apache2_repos": ["repo1"]
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos."""

    @classmethod
    def setUpClass(cls):
        """Set up patcher for requests.get."""
        cls.get_patcher = patch("client.requests.get")
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url, *args, **kwargs):
            if url == cls.org_payload["repos_url"]:
                mock_response = Mock()
                mock_response.json.return_value = cls.repos_payload
                return mock_response
            mock_response = Mock()
            mock_response.json.return_value = cls.org_payload
            return mock_response

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher for requests.get."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns all repository names."""
        client = GithubOrgClient("google")
        result = client.public_repos()
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos with license filter returns correct repos."""
        client = GithubOrgClient("google")
        result = client.public_repos(license="apache-2.0")
        self.assertEqual(result, self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
