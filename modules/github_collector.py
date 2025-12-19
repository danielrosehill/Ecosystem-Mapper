"""
GitHub API Data Collector

Searches GitHub for repositories matching a keyword from the last 3 months.
"""

import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from github import Github, GithubException
from dotenv import load_dotenv

load_dotenv()


class GitHubCollector:
    """Collects repository data from GitHub based on keyword searches."""

    def __init__(self):
        """Initialize GitHub API client."""
        github_token = os.getenv("GITHUB_PAT")
        if not github_token:
            raise ValueError("GITHUB_PAT environment variable not set")

        self.github = Github(github_token)
        self.rate_limit_info()

    def rate_limit_info(self):
        """Display current rate limit status."""
        rate_limit = self.github.get_rate_limit()
        print(f"GitHub API Rate Limit: {rate_limit.core.remaining}/{rate_limit.core.limit}")

    def search_repositories(
        self,
        keyword: str,
        months_back: int = 3,
        max_results: int = 100,
        min_stars: int = 0
    ) -> List[Dict]:
        """
        Search for repositories matching the keyword from recent months.

        Args:
            keyword: Search keyword (e.g., "agentic AI")
            months_back: How many months back to search (default: 3)
            max_results: Maximum number of results to return (default: 100)
            min_stars: Minimum number of stars (default: 0)

        Returns:
            List of repository dictionaries with metadata
        """
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=months_back * 30)
        date_query = f"created:>={start_date.strftime('%Y-%m-%d')}"

        # Build search query
        query_parts = [keyword, date_query]
        if min_stars > 0:
            query_parts.append(f"stars:>={min_stars}")

        query = " ".join(query_parts)

        print(f"Searching GitHub for: {query}")

        try:
            repositories = self.github.search_repositories(
                query=query,
                sort="stars",
                order="desc"
            )

            results = []
            count = 0

            for repo in repositories:
                if count >= max_results:
                    break

                repo_data = {
                    "name": repo.name,
                    "full_name": repo.full_name,
                    "description": repo.description or "",
                    "url": repo.html_url,
                    "stars": repo.stargazers_count,
                    "forks": repo.forks_count,
                    "language": repo.language,
                    "topics": repo.get_topics(),
                    "created_at": repo.created_at.isoformat(),
                    "updated_at": repo.updated_at.isoformat(),
                    "homepage": repo.homepage or "",
                    "license": repo.license.name if repo.license else None,
                }

                results.append(repo_data)
                count += 1

                if count % 10 == 0:
                    print(f"Collected {count} repositories...")

            print(f"Total repositories collected: {len(results)}")
            return results

        except GithubException as e:
            print(f"GitHub API error: {e}")
            return []

    def get_trending_topics(self, keyword: str, max_repos: int = 50) -> Dict[str, int]:
        """
        Extract trending topics from repositories matching the keyword.

        Args:
            keyword: Search keyword
            max_repos: Number of repos to analyze for topics

        Returns:
            Dictionary of topics and their frequency
        """
        repos = self.search_repositories(keyword, max_results=max_repos)

        topic_counts = {}
        for repo in repos:
            for topic in repo.get("topics", []):
                topic_counts[topic] = topic_counts.get(topic, 0) + 1

        # Sort by frequency
        sorted_topics = dict(
            sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)
        )

        return sorted_topics


def main():
    """Example usage."""
    collector = GitHubCollector()

    # Example search
    keyword = "agentic AI"
    repos = collector.search_repositories(keyword, max_results=20)

    print(f"\n{'='*80}")
    print(f"Top repositories for '{keyword}':")
    print(f"{'='*80}\n")

    for i, repo in enumerate(repos[:10], 1):
        print(f"{i}. {repo['full_name']} ({repo['stars']} ⭐)")
        print(f"   {repo['description'][:100]}...")
        print(f"   Topics: {', '.join(repo['topics'][:5])}")
        print()


if __name__ == "__main__":
    main()
