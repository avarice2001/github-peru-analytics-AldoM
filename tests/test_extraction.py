import pytest
from unittest.mock import Mock, patch
from src.extraction.github_client import GitHubClient
from src.extraction.user_extractor import UserExtractor


def test_github_client_init():
    with patch.dict("os.environ", {"GITHUB_TOKEN": "fake_token"}):
        client = GitHubClient()
        assert client.token == "fake_token"
        assert client.headers["Authorization"] == "token fake_token"


def test_user_extractor_search():
    client_mock = Mock()
    client_mock.make_request.return_value = {
        "items": [{"login": "user1"}, {"login": "user2"}]
    }
    extractor = UserExtractor(client_mock)
    users = extractor.search_users_by_location("Peru", max_users=2)
    assert len(users) == 2
    assert users[0]["login"] == "user1"
    client_mock.make_request.assert_called_once()
