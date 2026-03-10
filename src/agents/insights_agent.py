import os
import sqlite3
import pandas as pd
from openai import OpenAI
import json


class InsightsAgent:
    def __init__(self, db_path: str = "data/processed/"):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.db_path = db_path

    def query_local_data(self, query: str) -> str:
        """Simple data querying simulator for the agent tools."""
        try:
            # We can load data and provide context
            if "total developers" in query.lower() or "users" in query.lower():
                users = pd.read_csv(os.path.join(self.db_path, "users.csv"))
                return f"Total users: {len(users)}"
            if "repositories" in query.lower() or "repos" in query.lower():
                repos = pd.read_csv(os.path.join(self.db_path, "repositories.csv"))
                return f"Total repos: {len(repos)}"
            return "Query not understood or data not found."
        except Exception as e:
            return str(e)

    def analyze_ecosystem(self, question: str) -> str:
        """
        Analyze the ecosystem using an LLM based on user queries.
        This represents the agent logic.
        """
        system_prompt = """You are a Data Analysis Agent for the GitHub Peru Analytics project.
You have access to data about GitHub developers in Peru. Use your reasoning to answer questions about the ecosystem.
"""

        messages = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"Ecosystem question: {question}\n\nCan you tell me how to query this from my local CSVs or give a reasoned guess based on available metrics?",
            },
        ]

        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview", messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Agent error: {e}"
