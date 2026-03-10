import pandas as pd


class EcosystemMetrics:
    def __init__(
        self, users_df: pd.DataFrame, repos_df: pd.DataFrame, class_df: pd.DataFrame
    ):
        self.users_df = users_df
        self.repos_df = repos_df
        self.class_df = class_df

    def calculate_totals(self) -> dict:
        return {
            "total_developers": len(self.users_df),
            "total_repositories": len(self.repos_df),
            "total_stars": int(
                self.repos_df["stargazers_count"].sum()
                if "stargazers_count" in self.repos_df
                else 0
            ),
            "total_forks": int(
                self.repos_df["forks_count"].sum()
                if "forks_count" in self.repos_df
                else 0
            ),
        }

    def calculate_industry_distribution(self) -> dict:
        if self.class_df.empty or "industry_name" not in self.class_df:
            return {}
        return self.class_df["industry_name"].value_counts().to_dict()

    def calculate_language_distribution(self) -> dict:
        if "language" not in self.repos_df:
            return {}
        langs = self.repos_df["language"].dropna().value_counts()
        return langs.to_dict()

    def generate_report(self) -> dict:
        return {
            "totals": self.calculate_totals(),
            "industry_distribution": self.calculate_industry_distribution(),
            "language_distribution": self.calculate_language_distribution(),
        }
