"""
Taxonomy Analyzer

Uses Gemini Flash (via OpenRouter) to analyze collected data and create
ecosystem taxonomies with categorization and representative examples.
"""

import os
import json
from typing import List, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class TaxonomyAnalyzer:
    """Analyzes ecosystem data and creates taxonomies using AI."""

    def __init__(self):
        """Initialize OpenRouter client for Gemini."""
        api_key = os.getenv("OPENROUTER_API_KEY")
        model_name = os.getenv("OR_RESEARCH_MODEL_NAME", "google/gemini-3-flash-preview")

        if not api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable not set")

        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        self.model = model_name
        print(f"Initialized TaxonomyAnalyzer with model: {self.model}")

    def create_taxonomy(
        self,
        keyword: str,
        github_data: List[Dict],
        web_data: Dict[str, List[Dict]]
    ) -> Dict[str, Any]:
        """
        Create a taxonomy from GitHub and web data.

        Args:
            keyword: The search keyword
            github_data: List of GitHub repository data
            web_data: Dictionary of web search results by category

        Returns:
            Structured taxonomy with categories and examples
        """
        print(f"\nAnalyzing ecosystem for: {keyword}")
        print(f"Data sources: {len(github_data)} GitHub repos, {sum(len(v) for v in web_data.values())} web results")

        # Prepare data summary for AI analysis
        data_summary = self._prepare_data_summary(github_data, web_data)

        # Create the analysis prompt
        prompt = self._build_taxonomy_prompt(keyword, data_summary)

        try:
            print("\nRequesting taxonomy analysis from Gemini...")

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at analyzing technology ecosystems and creating structured taxonomies. You excel at identifying patterns, categories, and representative examples from raw data."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=4000
            )

            result = response.choices[0].message.content

            # Parse the JSON response
            taxonomy = json.loads(result)

            print(f"✓ Taxonomy created with {len(taxonomy.get('categories', []))} categories")

            return taxonomy

        except json.JSONDecodeError as e:
            print(f"Error parsing taxonomy JSON: {e}")
            print("Raw response:", result)
            return {"error": "Failed to parse taxonomy", "raw_response": result}
        except Exception as e:
            print(f"Error creating taxonomy: {e}")
            return {"error": str(e)}

    def _prepare_data_summary(
        self,
        github_data: List[Dict],
        web_data: Dict[str, List[Dict]]
    ) -> str:
        """Prepare a concise summary of the collected data."""
        summary_parts = []

        # GitHub repos summary
        summary_parts.append("=== GITHUB REPOSITORIES ===\n")
        for i, repo in enumerate(github_data[:30], 1):  # Limit to 30 repos
            summary_parts.append(
                f"{i}. {repo['full_name']} ({repo['stars']}⭐)\n"
                f"   Description: {repo['description']}\n"
                f"   Topics: {', '.join(repo['topics'][:5])}\n"
                f"   Language: {repo['language']}\n"
            )

        # Web results summary
        for category, results in web_data.items():
            summary_parts.append(f"\n=== WEB RESULTS: {category.upper()} ===\n")
            for i, result in enumerate(results[:15], 1):  # Limit to 15 per category
                summary_parts.append(
                    f"{i}. {result['title']}\n"
                    f"   URL: {result['url']}\n"
                    f"   Content: {result['content'][:200]}...\n"
                )

        return "\n".join(summary_parts)

    def _build_taxonomy_prompt(self, keyword: str, data_summary: str) -> str:
        """Build the prompt for taxonomy creation."""
        return f"""Analyze the following data about "{keyword}" and create a comprehensive ecosystem taxonomy.

DATA:
{data_summary}

TASK:
Create a structured taxonomy that:
1. Identifies 5-8 main categories within this ecosystem
2. For each category, identify 2-4 subcategories
3. Find 3-5 representative examples (projects/tools/companies) for each category
4. Describe the purpose and focus of each category
5. Identify relationships between categories (e.g., "builds on", "complements", "alternative to")

OUTPUT FORMAT (JSON):
{{
  "ecosystem_name": "{keyword}",
  "overview": "Brief 2-3 sentence overview of the ecosystem",
  "categories": [
    {{
      "name": "Category Name",
      "description": "What this category focuses on",
      "subcategories": ["Subcategory 1", "Subcategory 2"],
      "examples": [
        {{
          "name": "Project/Tool Name",
          "description": "Brief description",
          "url": "URL if available",
          "type": "open-source|commercial|framework|library|platform"
        }}
      ],
      "relationships": ["Related to X", "Built on Y"]
    }}
  ],
  "key_trends": ["Trend 1", "Trend 2", "Trend 3"],
  "emerging_areas": ["Area 1", "Area 2"]
}}

Respond ONLY with valid JSON. Do not include any markdown formatting or additional text."""

    def enrich_taxonomy(self, taxonomy: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enrich the taxonomy with additional insights.

        Args:
            taxonomy: The base taxonomy

        Returns:
            Enhanced taxonomy with insights
        """
        if "error" in taxonomy:
            return taxonomy

        prompt = f"""Given this ecosystem taxonomy:

{json.dumps(taxonomy, indent=2)}

Provide additional insights:
1. Market maturity assessment (emerging, growing, mature)
2. Key differentiators between categories
3. Gaps or underserved areas in the ecosystem
4. Potential convergence or integration opportunities

OUTPUT FORMAT (JSON):
{{
  "maturity_level": "emerging|growing|mature",
  "maturity_analysis": "Brief explanation",
  "category_differentiators": {{"Category1": "Key differentiator", "Category2": "Key differentiator"}},
  "ecosystem_gaps": ["Gap 1", "Gap 2"],
  "integration_opportunities": ["Opportunity 1", "Opportunity 2"]
}}

Respond ONLY with valid JSON."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert technology ecosystem analyst."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )

            insights = json.loads(response.choices[0].message.content)
            taxonomy["insights"] = insights

            print("✓ Taxonomy enriched with additional insights")

            return taxonomy

        except Exception as e:
            print(f"Error enriching taxonomy: {e}")
            return taxonomy


def main():
    """Example usage."""
    # This would normally be called with real data from collectors
    analyzer = TaxonomyAnalyzer()

    # Mock data for testing
    mock_github_data = [
        {
            "full_name": "example/agent-framework",
            "description": "A framework for building AI agents",
            "stars": 1500,
            "topics": ["ai", "agents", "llm"],
            "language": "Python"
        }
    ]

    mock_web_data = {
        "general": [
            {
                "title": "Introduction to Agentic AI",
                "url": "https://example.com/article",
                "content": "Agentic AI refers to AI systems that can act autonomously...",
                "score": 0.95
            }
        ]
    }

    taxonomy = analyzer.create_taxonomy(
        keyword="agentic AI",
        github_data=mock_github_data,
        web_data=mock_web_data
    )

    print("\n" + "="*80)
    print("TAXONOMY RESULT:")
    print("="*80)
    print(json.dumps(taxonomy, indent=2))


if __name__ == "__main__":
    main()
