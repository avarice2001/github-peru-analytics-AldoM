import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import json
from src.metrics.user_metrics import UserMetrics
from src.metrics.ecosystem_metrics import EcosystemMetrics


def main():
    print("Loading processed data...")
    try:
        users_df = pd.read_csv("data/processed/users.csv")
        repos_df = pd.read_csv("data/processed/repositories.csv")
        class_df = pd.read_csv("data/processed/classifications.csv")
    except FileNotFoundError as e:
        print(f"Data file missing: {e}")
        return

    print("Calculating User Metrics...")
    user_metrics_calculator = UserMetrics(users_df, repos_df)
    user_metrics_df = user_metrics_calculator.calculate_all_metrics()

    print("Saving User Metrics...")
    user_metrics_df.to_csv("data/metrics/user_metrics.csv", index=False)

    print("Calculating Ecosystem Metrics...")
    eco_metrics_calculator = EcosystemMetrics(users_df, repos_df, class_df)
    eco_metrics_dict = eco_metrics_calculator.generate_report()

    print("Saving Ecosystem Metrics...")
    with open("data/metrics/ecosystem_metrics.json", "w") as f:
        json.dump(eco_metrics_dict, f, indent=4)

    print("Metrics calculation complete!")


if __name__ == "__main__":
    main()
