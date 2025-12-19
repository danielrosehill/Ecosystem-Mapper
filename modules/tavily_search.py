"""
Tavily Web Search Integration

Performs web searches to find articles, tools, and resources related to the keyword.
"""

import os
from typing import List, Dict, Optional
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()


class TavilySearcher:
    """Performs web searches using Tavily API."""

    def __init__(self):
        """Initialize Tavily client."""
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            raise ValueError("TAVILY_API_KEY environment variable not set")

        self.client = TavilyClient(api_key=api_key)

    def search(
        self,
        keyword: str,
        max_results: int = 20,
        search_depth: str = "advanced",
        include_domains: Optional[List[str]] = None,
        exclude_domains: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        Search the web for content related to the keyword.

        Args:
            keyword: Search keyword (e.g., "agentic AI frameworks")
            max_results: Maximum number of results (default: 20)
            search_depth: "basic" or "advanced" (default: "advanced")
            include_domains: List of domains to prioritize
            exclude_domains: List of domains to exclude

        Returns:
            List of search result dictionaries
        """
        print(f"Searching web for: {keyword}")

        try:
            response = self.client.search(
                query=keyword,
                max_results=max_results,
                search_depth=search_depth,
                include_domains=include_domains or [],
                exclude_domains=exclude_domains or []
            )

            results = []
            for item in response.get("results", []):
                result = {
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "content": item.get("content", ""),
                    "score": item.get("score", 0),
                    "published_date": item.get("published_date", "")
                }
                results.append(result)

            print(f"Found {len(results)} web results")
            return results

        except Exception as e:
            print(f"Tavily search error: {e}")
            return []

    def search_tools_and_projects(
        self,
        keyword: str,
        max_results: int = 15
    ) -> List[Dict]:
        """
        Search specifically for tools, libraries, and projects.

        Args:
            keyword: Search keyword
            max_results: Maximum results

        Returns:
            List of tool/project search results
        """
        # Enhance query to find tools and projects
        enhanced_query = f"{keyword} tools libraries frameworks projects"

        # Prioritize technical domains
        include_domains = [
            "github.com",
            "gitlab.com",
            "pypi.org",
            "npmjs.com",
            "arxiv.org",
            "huggingface.co"
        ]

        return self.search(
            keyword=enhanced_query,
            max_results=max_results,
            include_domains=include_domains
        )

    def search_ecosystem_overview(
        self,
        keyword: str,
        max_results: int = 10
    ) -> List[Dict]:
        """
        Search for ecosystem overviews, market maps, and landscape analyses.

        Args:
            keyword: Search keyword
            max_results: Maximum results

        Returns:
            List of ecosystem analysis results
        """
        # Enhance query to find ecosystem content
        enhanced_query = f"{keyword} ecosystem landscape market map overview"

        return self.search(
            keyword=enhanced_query,
            max_results=max_results,
            search_depth="advanced"
        )

    def combine_searches(self, keyword: str) -> Dict[str, List[Dict]]:
        """
        Perform multiple search types and combine results.

        Args:
            keyword: Search keyword

        Returns:
            Dictionary with different search result categories
        """
        print(f"\n{'='*80}")
        print(f"Comprehensive Web Search for: {keyword}")
        print(f"{'='*80}\n")

        results = {
            "general": self.search(keyword, max_results=15),
            "tools": self.search_tools_and_projects(keyword, max_results=15),
            "ecosystem": self.search_ecosystem_overview(keyword, max_results=10)
        }

        total = sum(len(v) for v in results.values())
        print(f"\nTotal web results collected: {total}")

        return results


def main():
    """Example usage."""
    searcher = TavilySearcher()

    # Example search
    keyword = "agentic AI"
    results = searcher.combine_searches(keyword)

    print(f"\n{'='*80}")
    print(f"Search Results Summary for '{keyword}':")
    print(f"{'='*80}\n")

    for category, items in results.items():
        print(f"\n{category.upper()} ({len(items)} results):")
        print("-" * 40)
        for i, item in enumerate(items[:5], 1):
            print(f"{i}. {item['title']}")
            print(f"   URL: {item['url']}")
            print(f"   Score: {item['score']:.2f}")
            print()


if __name__ == "__main__":
    main()
