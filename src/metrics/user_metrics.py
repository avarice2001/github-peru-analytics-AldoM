import pandas as pd
import json


class UserMetrics:
    def __init__(self, users_df: pd.DataFrame, repos_df: pd.DataFrame):
        self.users_df = users_df
        self.repos_df = repos_df
        # Create a helper dict for repos by owner
        self.repos_by_owner = {}
        for _, repo in self.repos_df.iterrows():
            owner_val = repo.get("owner", "")
            if isinstance(owner_val, str) and owner_val.startswith("{"):
                import ast
                try:
                    owner = ast.literal_eval(owner_val).get("login", "")
                except:
                    owner = ""
            elif isinstance(owner_val, dict):
                owner = owner_val.get("login", "")
            else:
                owner = repo.get("owner_login", "")

            if not owner or pd.isna(owner):
                continue
            if owner not in self.repos_by_owner:
                self.repos_by_owner[owner] = []
            self.repos_by_owner[owner].append(repo)

    def calculate_activity_metrics(self, username: str) -> dict:
        user_repos = self.repos_by_owner.get(username, [])
        total_repos = len(user_repos)
        # Note: accurate commit count requires more API calls, we use simplified versions or placeholders
        total_commits = sum(repo.get("size", 0) for repo in user_repos)  # proxy for now
        days_active = 365  # proxy, requires full events API

        return {
            "total_repositories": total_repos,
            "total_commits": total_commits,
            "days_active": days_active,
        }

    def calculate_influence_metrics(self, username: str, user_data: pd.Series) -> dict:
        user_repos = self.repos_by_owner.get(username, [])
        total_followers = user_data.get("followers", 0)
        total_stars = sum(repo.get("stargazers_count", 0) for repo in user_repos)
        total_forks = sum(repo.get("forks_count", 0) for repo in user_repos)

        # Simple influence score formula
        influence_score = (
            (total_followers * 2) + (total_stars * 3) + (total_forks * 1.5)
        )

        return {
            "total_followers": total_followers,
            "total_stars": total_stars,
            "total_forks": total_forks,
            "influence_score": influence_score,
        }

    def calculate_technical_metrics(self, username: str) -> dict:
        user_repos = self.repos_by_owner.get(username, [])
        languages = set()
        for repo in user_repos:
            lang = repo.get("language")
            if lang and pd.notna(lang):
                languages.add(lang)
            # check languages_dict if extracted
            langs_dict_str = repo.get("languages_dict", "{}")
            if pd.notna(langs_dict_str) and langs_dict_str:
                try:
                    langs_dict = json.loads(langs_dict_str)
                    languages.update(langs_dict.keys())
                except:
                    pass

        return {
            "primary_language": list(languages)[0] if languages else "None",
            "languages_used": len(languages),
            "complexity_score": len(languages) * 2
            + sum(repo.get("size", 0) for repo in user_repos) / 1000,
        }

    def calculate_all_metrics(self) -> pd.DataFrame:
        results = []
        for _, user in self.users_df.iterrows():
            username = user["login"]
            activity = self.calculate_activity_metrics(username)
            influence = self.calculate_influence_metrics(username, user)
            technical = self.calculate_technical_metrics(username)

            user_metric = {"username": username, **activity, **influence, **technical}
            results.append(user_metric)

        return pd.DataFrame(results)
