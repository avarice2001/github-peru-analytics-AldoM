import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.extraction.github_client import GitHubClient
from src.extraction.user_extractor import UserExtractor
from src.extraction.repo_extractor import RepoExtractor


def process_repo(repo, repo_ext):
    repo_info = repo.copy()
    owner = repo["owner"]["login"]
    repo_name = repo["name"]
    # Enrich repo data
    readme = repo_ext.get_repo_readme(owner, repo_name)
    languages = repo_ext.get_repo_languages(owner, repo_name)
    repo_info["readme"] = readme
    repo_info["languages_dict"] = json.dumps(languages)
    return repo_info


def main():
    client = GitHubClient()
    user_ext = UserExtractor(client)
    repo_ext = RepoExtractor(client)

    print("Fetching users from Peru...")
    # Searching by location:Peru, location:Lima, etc. could yield more.
    # We will just fetch 1000 from Peru directly for now
    users = user_ext.search_users_by_location("Peru", max_users=1000)
    print(f"Found {len(users)} users.")

    user_data = []
    repo_data = []

    # We need at least 1000 repos.
    # We will iter through users and get their repos until we hit the target.

    for user in tqdm(users, desc="Processing users and their repos"):
        username = user["login"]

        # Get details
        details = user_ext.get_user_details(username)
        if details:
            user_data.append(details)

        # Get repos
        repos = user_ext.get_user_repos(username)
        # Process at most 30 repos per user to avoid getting stuck
        repos = repos[:30]
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_repo = {executor.submit(process_repo, repo, repo_ext): repo for repo in repos}
            for future in as_completed(future_to_repo):
                try:
                    repo_info = future.result()
                    repo_data.append(repo_info)
                except Exception as e:
                    print(f"Error processing repo: {e}")

            # Save intermediate occasionally or break if enough
            if len(repo_data) >= 1200:  # get a bit extra
                break

        if len(repo_data) >= 1200:
            break

    print(f"Collected {len(user_data)} users and {len(repo_data)} repos.")

    # Save data
    pd.DataFrame(user_data).to_csv("data/raw/users/users.csv", index=False)
    pd.DataFrame(repo_data).to_csv("data/raw/repos/repos.csv", index=False)
    print("Data saved to data/raw/users/ and data/raw/repos/")


if __name__ == "__main__":
    main()
