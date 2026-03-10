from .github_client import GitHubClient
import base64


class RepoExtractor:
    def __init__(self, client: GitHubClient):
        self.client = client

    def get_repo_readme(self, owner: str, repo: str) -> str:
        """
        Get the README content of a repository.
        Returns empty string if not found.
        """
        try:
            result = self.client.make_request(f"repos/{owner}/{repo}/readme")
            content = base64.b64decode(result["content"]).decode(
                "utf-8", errors="ignore"
            )
            return content[:5000]  # Limit to 5000 chars for API costs
        except Exception:
            return ""

    def get_repo_languages(self, owner: str, repo: str) -> dict:
        """Get the language breakdown of a repository."""
        try:
            return self.client.make_request(f"repos/{owner}/{repo}/languages")
        except Exception:
            return {}

    def get_repo_contributors(self, owner: str, repo: str) -> list[dict]:
        """Get the contributors of a repository."""
        try:
            return self.client.make_request(
                f"repos/{owner}/{repo}/contributors", params={"per_page": 100}
            )
        except Exception:
            return []
