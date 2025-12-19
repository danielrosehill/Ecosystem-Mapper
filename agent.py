#!/usr/bin/env python3
"""
Ecosystem Mapper Agent

Main orchestration script that coordinates data collection, analysis, and taxonomy generation.
"""

import os
import json
import click
from datetime import datetime
from pathlib import Path

from modules.github_collector import GitHubCollector
from modules.tavily_search import TavilySearcher
from modules.taxonomy_analyzer import TaxonomyAnalyzer


class EcosystemMapper:
    """Main agent for ecosystem mapping."""

    def __init__(self):
        """Initialize the ecosystem mapper with all modules."""
        print("Initializing Ecosystem Mapper...")
        self.github_collector = GitHubCollector()
        self.tavily_searcher = TavilySearcher()
        self.taxonomy_analyzer = TaxonomyAnalyzer()

        # Ensure outputs directory exists
        self.outputs_dir = Path("outputs")
        self.outputs_dir.mkdir(exist_ok=True)
        print("✓ All modules initialized\n")

    def map_ecosystem(
        self,
        keyword: str,
        max_github_repos: int = 50,
        months_back: int = 3,
        enrich: bool = True,
        save_raw: bool = True
    ) -> dict:
        """
        Complete ecosystem mapping workflow.

        Args:
            keyword: The ecosystem keyword to analyze
            max_github_repos: Maximum GitHub repositories to collect
            months_back: How many months back to search GitHub
            enrich: Whether to enrich taxonomy with additional insights
            save_raw: Whether to save raw collected data

        Returns:
            Complete taxonomy dictionary
        """
        print("="*80)
        print(f"ECOSYSTEM MAPPING: {keyword}")
        print("="*80)
        print()

        # Stage 1: Data Collection
        print("STAGE 1: DATA COLLECTION")
        print("-"*80)

        # Collect GitHub data
        print("\n[1/2] Collecting GitHub repositories...")
        github_data = self.github_collector.search_repositories(
            keyword=keyword,
            max_results=max_github_repos,
            months_back=months_back
        )

        # Collect web data
        print("\n[2/2] Collecting web search results...")
        web_data = self.tavily_searcher.combine_searches(keyword)

        # Save raw data if requested
        if save_raw:
            self._save_raw_data(keyword, github_data, web_data)

        # Stage 2: Taxonomy Analysis
        print("\n" + "="*80)
        print("STAGE 2: TAXONOMY ANALYSIS")
        print("-"*80)

        taxonomy = self.taxonomy_analyzer.create_taxonomy(
            keyword=keyword,
            github_data=github_data,
            web_data=web_data
        )

        # Enrich taxonomy if requested
        if enrich and "error" not in taxonomy:
            print("\nEnriching taxonomy with insights...")
            taxonomy = self.taxonomy_analyzer.enrich_taxonomy(taxonomy)

        # Save taxonomy
        self._save_taxonomy(keyword, taxonomy)

        # Print summary
        self._print_summary(taxonomy)

        return taxonomy

    def _save_raw_data(self, keyword: str, github_data: list, web_data: dict):
        """Save raw collected data to files."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_keyword = keyword.replace(" ", "_").replace("/", "-")

        raw_data = {
            "keyword": keyword,
            "timestamp": timestamp,
            "github_repositories": github_data,
            "web_results": web_data
        }

        filename = self.outputs_dir / f"{safe_keyword}_raw_data_{timestamp}.json"

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(raw_data, f, indent=2, ensure_ascii=False)

        print(f"\n✓ Raw data saved to: {filename}")

    def _save_taxonomy(self, keyword: str, taxonomy: dict):
        """Save taxonomy to file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_keyword = keyword.replace(" ", "_").replace("/", "-")

        filename = self.outputs_dir / f"{safe_keyword}_taxonomy_{timestamp}.json"

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(taxonomy, f, indent=2, ensure_ascii=False)

        print(f"\n✓ Taxonomy saved to: {filename}")

        # Also save a "latest" version
        latest_filename = self.outputs_dir / f"{safe_keyword}_taxonomy_latest.json"
        with open(latest_filename, "w", encoding="utf-8") as f:
            json.dump(taxonomy, f, indent=2, ensure_ascii=False)

        print(f"✓ Latest taxonomy: {latest_filename}")

    def _print_summary(self, taxonomy: dict):
        """Print a summary of the taxonomy."""
        print("\n" + "="*80)
        print("TAXONOMY SUMMARY")
        print("="*80)

        if "error" in taxonomy:
            print(f"\n❌ Error: {taxonomy['error']}")
            return

        print(f"\nEcosystem: {taxonomy.get('ecosystem_name', 'Unknown')}")
        print(f"\nOverview: {taxonomy.get('overview', 'N/A')}")

        categories = taxonomy.get('categories', [])
        print(f"\nCategories ({len(categories)}):")

        for i, category in enumerate(categories, 1):
            examples_count = len(category.get('examples', []))
            subcategories_count = len(category.get('subcategories', []))

            print(f"\n{i}. {category['name']}")
            print(f"   Description: {category['description']}")
            print(f"   Subcategories: {subcategories_count}")
            print(f"   Examples: {examples_count}")

            # Show first few examples
            for example in category.get('examples', [])[:3]:
                print(f"     - {example['name']}: {example.get('description', 'N/A')[:60]}...")

        # Show key trends if available
        if 'key_trends' in taxonomy:
            print(f"\nKey Trends:")
            for trend in taxonomy['key_trends']:
                print(f"  • {trend}")

        # Show insights if available
        if 'insights' in taxonomy:
            insights = taxonomy['insights']
            print(f"\nInsights:")
            print(f"  Maturity: {insights.get('maturity_level', 'N/A')}")
            if 'ecosystem_gaps' in insights:
                print(f"  Gaps identified: {len(insights['ecosystem_gaps'])}")

        print("\n" + "="*80)


@click.command()
@click.option(
    '--keyword',
    '-k',
    required=True,
    help='Ecosystem keyword to analyze (e.g., "agentic AI")'
)
@click.option(
    '--max-repos',
    '-m',
    default=50,
    help='Maximum GitHub repositories to collect (default: 50)'
)
@click.option(
    '--months',
    '-t',
    default=3,
    help='How many months back to search GitHub (default: 3)'
)
@click.option(
    '--no-enrich',
    is_flag=True,
    help='Skip taxonomy enrichment step'
)
@click.option(
    '--no-save-raw',
    is_flag=True,
    help='Do not save raw collected data'
)
def main(keyword, max_repos, months, no_enrich, no_save_raw):
    """
    Ecosystem Mapper Agent

    Automatically discovers, analyzes, and categorizes technology ecosystems.

    Example usage:

        python agent.py --keyword "agentic AI"

        python agent.py -k "vector databases" --max-repos 100

        python agent.py -k "RAG frameworks" --months 6 --no-enrich
    """
    try:
        mapper = EcosystemMapper()

        taxonomy = mapper.map_ecosystem(
            keyword=keyword,
            max_github_repos=max_repos,
            months_back=months,
            enrich=not no_enrich,
            save_raw=not no_save_raw
        )

        print("\n✅ Ecosystem mapping complete!")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)


if __name__ == "__main__":
    main()
