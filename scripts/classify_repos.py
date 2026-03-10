import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from dotenv import load_dotenv
from src.classification.industry_classifier import IndustryClassifier

load_dotenv()


def main():
    print("Loading raw repositories...")
    try:
        repos_df = pd.read_csv("data/raw/repos/repos.csv")
    except FileNotFoundError:
        print("Repos file not found. Run extract_data.py first.")
        return

    # Convert DataFrame to list of dicts for the classifier
    # It might contain NaN for some fields, replace with empty strings/lists
    repos_df = repos_df.fillna("")

    # We need 'topics' as a list. Assume it's a list or string representation
    def parse_topics(val):
        if isinstance(val, str) and val:
            try:
                import ast

                val = ast.literal_eval(val)
            except:
                val = []
        if not isinstance(val, list):
            val = []
        return val

    if "topics" in repos_df.columns:
        repos_df["topics"] = repos_df["topics"].apply(parse_topics)
    else:
        repos_df["topics"] = [[] for _ in range(len(repos_df))]

    repositories = repos_df.to_dict("records")

    classifier = IndustryClassifier()
    print("Starting classification...")
    classified_data = classifier.batch_classify(repositories, batch_size=20)

    print("Saving classification results...")
    classifications_df = pd.DataFrame(classified_data)
    classifications_df.to_csv("data/processed/classifications.csv", index=False)

    # Also save a cleaned version of repos and users
    users_df = pd.read_csv("data/raw/users/users.csv")
    users_df.to_csv("data/processed/users.csv", index=False)
    repos_df.to_csv("data/processed/repositories.csv", index=False)

    print("Processing complete!")


if __name__ == "__main__":
    main()
