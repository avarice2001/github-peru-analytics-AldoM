from .github_client import GitHubClient


class UserExtractor:
    def __init__(self, client: GitHubClient):
        self.client = client

    def search_users_by_location(
        self, location: str, max_users: int = 1000
    ) -> list[dict]:
        """
        Search for users by location.
        """
        users = []
        page = 1
        per_page = 100

        while len(users) < max_users:
            try:
                result = self.client.make_request(
                    "search/users",
                    params={
                        "q": f"location:{location}",
                        "per_page": per_page,
                        "page": page,
                        "sort": "followers",
                        "order": "desc",
                    },
                )

                if not result.get("items"):
                    break

                users.extend(result["items"])
                page += 1

                # GitHub search API limits to 1000 results
                if page * per_page > 1000:
                    break
            except Exception as e:
                print(f"Error searching users on page {page}: {e}")
                break

        return users[:max_users]

    def get_user_details(self, username: str) -> dict:
        """Get detailed information for a specific user."""
        try:
            return self.client.make_request(f"users/{username}")
        except Exception as e:
            print(f"Error getting details for user {username}: {e}")
            return {}

    def get_user_repos(self, username: str) -> list[dict]:
        """Get all repositories for a user."""
        repos = []
        page = 1
        while True:
            try:
                result = self.client.make_request(
                    f"users/{username}/repos",
                    params={"per_page": 100, "page": page, "type": "owner"},
                )

                if not result:
                    break

                repos.extend(result)
                page += 1
            except Exception as e:
                print(f"Error getting repos for user {username} on page {page}: {e}")
                break

        return repos
