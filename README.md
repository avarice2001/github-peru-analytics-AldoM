# GitHub Peru Analytics

## 1. Project Title and Description
GitHub Peru Analytics is a comprehensive platform designed to extract, process, classify, and visualize data from over 1,000 GitHub developers specifically located in Peru. It uses the GitHub API, OpenAI's GPT-4, and Streamlit to provide actionable insights.

## 2. Key Findings
- *Example Finding 1*: E.g., The most popular programming language is Python.
- *Example Finding 2*: E.g., The Information and communication industry is the most prominent.
- *Example Finding 3*: Many developers contribute to open source but don't explicitly list their industry.

## 3. Data Collection
We collected data using the GitHub REST API (`https://api.github.com/search/users?q=location:Peru`) and subsequently queried individual user and repository endpoints with retry logic and wait conditions applied to circumvent API rate limits.

## 4. Features
- **API Extraction**: Robust, rate-limit-aware extraction using tenacity.
- **AI Classification**: GPT-4 driven classification mapping repositories to 21 Peruvian industry codes.
- **Metrics Calculation**: Comprehensive Activity, Influence, and Technical metrics.
- **Interactive Dashboard**: A 5-page Streamlit application providing deep dives into developers, repositories, languages, and industries.

## 5. Installation
1. Clone the repository.
2. Initialize environment: `python -m venv .venv` and source it.
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and fill your `GITHUB_TOKEN` and `OPENAI_API_KEY`.

## 6. Usage
```bash
# 1. Extract data
python scripts/extract_data.py

# 2. Classify repos
python scripts/classify_repos.py

# 3. Calculate metrics
python scripts/calculate_metrics.py

# 4. Start dashboard
streamlit run app/main.py
```

## 7. Metrics Documentation
- **Activity Metrics**: `total_repositories`, `total_commits` (proxied by size), `days_active`
- **Influence Metrics**: `influence_score` calculated as (followers*2) + (stars*3) + (forks*1.5)
- **Technical Metrics**: `primary_language`, `languages_used`, `complexity_score`

## 8. AI Agent Documentation
The project includes a simple `InsightsAgent` demonstrating how an LLM can analyze the ecosystem. It is intended to interface with the local CSV data securely.

## 9. Limitations
- GitHub limits the search API to 1000 results. To get more, we would need to specify locations by city (Lima, Arequipa, etc.).
- Commit counts are proxied by repository size due to the high volume of API calls required to fetch complete commit histories.

## 10. Author Information
Developed by Antigravity Assistant.
