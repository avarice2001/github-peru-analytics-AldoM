import pytest
import pandas as pd
from src.metrics.user_metrics import UserMetrics
from src.metrics.ecosystem_metrics import EcosystemMetrics


@pytest.fixture
def mock_data():
    users = pd.DataFrame(
        [{"login": "dev1", "followers": 10}, {"login": "dev2", "followers": 20}]
    )
    repos = pd.DataFrame(
        [
            {
                "owner": {"login": "dev1"},
                "name": "repo1",
                "stargazers_count": 5,
                "forks_count": 2,
                "size": 100,
                "language": "Python",
            },
            {
                "owner": {"login": "dev1"},
                "name": "repo2",
                "stargazers_count": 10,
                "forks_count": 5,
                "size": 200,
                "language": "JavaScript",
            },
            {
                "owner": {"login": "dev2"},
                "name": "repo3",
                "stargazers_count": 50,
                "forks_count": 10,
                "size": 1000,
                "language": "Python",
            },
        ]
    )
    class_df = pd.DataFrame(
        [
            {"repo_id": 1, "industry_name": "Information and communication"},
            {"repo_id": 2, "industry_name": "Finance"},
            {"repo_id": 3, "industry_name": "Information and communication"},
        ]
    )
    return users, repos, class_df


def test_user_metrics_influence(mock_data):
    users, repos, _ = mock_data
    um = UserMetrics(users, repos)

    # Dev1: (10 followers * 2) + (15 stars * 3) + (7 forks * 1.5) = 20 + 45 + 10.5 = 75.5
    dev1_influence = um.calculate_influence_metrics("dev1", users.iloc[0])
    assert dev1_influence["influence_score"] == 75.5
    assert dev1_influence["total_stars"] == 15


def test_ecosystem_metrics_totals(mock_data):
    users, repos, class_df = mock_data
    em = EcosystemMetrics(users, repos, class_df)

    totals = em.calculate_totals()
    assert totals["total_developers"] == 2
    assert totals["total_repositories"] == 3
    assert totals["total_stars"] == 65
