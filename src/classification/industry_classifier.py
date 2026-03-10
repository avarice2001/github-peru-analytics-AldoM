import os
from openai import OpenAI
import json
from tqdm import tqdm


class IndustryClassifier:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.industries = {
            "A": "Agriculture, forestry and fishing",
            "B": "Mining and quarrying",
            "C": "Manufacturing",
            "D": "Electricity, gas, steam supply",
            "E": "Water supply; sewerage",
            "F": "Construction",
            "G": "Wholesale and retail trade",
            "H": "Transportation and storage",
            "I": "Accommodation and food services",
            "J": "Information and communication",
            "K": "Financial and insurance activities",
            "L": "Real estate activities",
            "M": "Professional, scientific activities",
            "N": "Administrative and support activities",
            "O": "Public administration and defense",
            "P": "Education",
            "Q": "Human health and social work",
            "R": "Arts, entertainment and recreation",
            "S": "Other service activities",
            "T": "Activities of households",
            "U": "Extraterritorial organizations",
        }

    def classify_repository(
        self, name: str, description: str, readme: str, topics: list[str], language: str
    ) -> dict:
        """
        Classify a repository into an industry category.
        """
        if not description:
            description = "No description"
        if not readme:
            readme = "No README"
        if not language:
            language = "Not specified"
        topics_str = ", ".join(topics) if topics else "None"

        prompt = f"""Analyze this GitHub repository and classify it into ONE of the following industry categories based on its potential application or the industry it serves.

REPOSITORY INFORMATION:
- Name: {name}
- Description: {description}
- Primary Language: {language}
- Topics: {topics_str}
- README (first 2000 chars): {readme[:2000]}

INDUSTRY CATEGORIES:
{json.dumps(self.industries, indent=2)}

INSTRUCTIONS:
1. Analyze the repository's purpose, functionality, and potential use cases
2. Consider what industry would most benefit from or use this software
3. If it's a general-purpose tool (e.g., utility library), classify based on the most likely industry application
4. If truly generic (e.g., "hello world"), use "J" (Information and communication)

Respond in JSON format:
{{
    "industry_code": "X",
    "industry_name": "Full industry name",
    "confidence": "high|medium|low",
    "reasoning": "Brief explanation of why this classification was chosen"
}}
"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at classifying software projects by industry. Always respond with valid JSON.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                response_format={"type": "json_object"},
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Error classifying repo {name}: {e}")
            return {
                "industry_code": "J",
                "industry_name": self.industries["J"],
                "confidence": "low",
                "reasoning": f"Classification failed: {e}",
            }

    def batch_classify(
        self, repositories: list[dict], batch_size: int = 20
    ) -> list[dict]:
        """
        Classify multiple repositories efficiently.
        """
        from concurrent.futures import ThreadPoolExecutor, as_completed
        results = []
        
        def process(repo):
            return {
                "repo_id": repo.get("id"),
                "repo_name": repo.get("name"),
                **self.classify_repository(
                    name=repo.get("name", ""),
                    description=repo.get("description", ""),
                    readme=repo.get("readme", ""),
                    topics=repo.get("topics", []),
                    language=repo.get("language", "")
                )
            }
            
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_repo = {executor.submit(process, repo): repo for repo in repositories}
            for future in tqdm(as_completed(future_to_repo), total=len(repositories), desc="Classifying repos"):
                try:
                    results.append(future.result())
                except Exception as e:
                    print(f"Error: {e}")
                    
        return results
