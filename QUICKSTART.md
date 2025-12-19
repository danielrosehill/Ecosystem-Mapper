# Quick Start Guide

## Installation

1. **Clone the repository** (if not already done):
```bash
cd ~/repos/github
git clone <repository-url>
cd Ecosystem-Mapper
```

2. **Set up Python environment**:
```bash
# Using uv (recommended)
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

# Or using standard venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. **Configure environment variables**:
```bash
# Copy example and edit with your API keys
cp .env.example .env
nano .env  # or use your preferred editor
```

Required API keys:
- **OpenRouter API Key**: Get from [openrouter.ai](https://openrouter.ai)
- **GitHub PAT**: Create at [github.com/settings/tokens](https://github.com/settings/tokens)
- **Tavily API Key**: Get from [tavily.com](https://tavily.com)

## Basic Usage

### Analyze an Ecosystem

```bash
# Basic analysis
python agent.py --keyword "agentic AI"

# With custom parameters
python agent.py --keyword "vector databases" --max-repos 100 --months 6

# Skip enrichment (faster)
python agent.py --keyword "MLOps tools" --no-enrich
```

### Command-Line Options

- `--keyword`, `-k`: Ecosystem keyword to analyze (required)
- `--max-repos`, `-m`: Max GitHub repos to collect (default: 50)
- `--months`, `-t`: How many months back to search (default: 3)
- `--no-enrich`: Skip taxonomy enrichment step
- `--no-save-raw`: Don't save raw collected data

### Example Workflows

**Quick exploration:**
```bash
python agent.py -k "RAG frameworks" --max-repos 30 --no-enrich
```

**Comprehensive analysis:**
```bash
python agent.py -k "agentic AI" --max-repos 100 --months 6
```

**Recent projects only:**
```bash
python agent.py -k "LangGraph alternatives" --months 1
```

## Output

The agent generates:

1. **Taxonomy JSON** (`outputs/<keyword>_taxonomy_<timestamp>.json`):
   - Ecosystem overview
   - Categories and subcategories
   - Representative examples
   - Key trends and insights

2. **Latest Taxonomy** (`outputs/<keyword>_taxonomy_latest.json`):
   - Always points to the most recent analysis

3. **Raw Data** (`outputs/<keyword>_raw_data_<timestamp>.json`):
   - GitHub repositories collected
   - Web search results
   - Useful for debugging or custom analysis

## Output Structure

```json
{
  "ecosystem_name": "agentic AI",
  "overview": "Brief ecosystem description",
  "categories": [
    {
      "name": "Category Name",
      "description": "What this focuses on",
      "subcategories": ["Sub1", "Sub2"],
      "examples": [
        {
          "name": "Project Name",
          "description": "Brief description",
          "url": "https://...",
          "type": "open-source|commercial|framework|..."
        }
      ],
      "relationships": ["Related to X"]
    }
  ],
  "key_trends": ["Trend 1", "Trend 2"],
  "emerging_areas": ["Area 1"],
  "insights": {
    "maturity_level": "emerging|growing|mature",
    "ecosystem_gaps": ["Gap 1"],
    "integration_opportunities": ["Opp 1"]
  }
}
```

## Testing Individual Modules

### GitHub Collector
```bash
python -m modules.github_collector
```

### Tavily Search
```bash
python -m modules.tavily_search
```

### Taxonomy Analyzer
```bash
python -m modules.taxonomy_analyzer
```

## Troubleshooting

### Rate Limits

**GitHub API**: 5,000 requests/hour (authenticated)
- Check remaining: The agent displays this at startup
- Solution: Wait or use fewer repos (`--max-repos`)

**OpenRouter**: Varies by model
- Check your usage at openrouter.ai
- Solution: Use fewer requests or upgrade plan

**Tavily**: Depends on your plan
- Check your plan limits
- Solution: Reduce search scope

### Common Errors

**"GITHUB_PAT environment variable not set"**
- Ensure `.env` file exists with `GITHUB_PAT=your_token`
- Activate your virtual environment

**"Error creating taxonomy: ..."**
- Check OpenRouter API key is valid
- Verify you have credits/quota remaining
- Try with `--no-enrich` to reduce API calls

**"Tavily search error: ..."**
- Verify `TAVILY_API_KEY` is correct
- Check you haven't exceeded your plan limits

## Next Steps

1. **Run your first analysis**: Start with a topic you know well
2. **Explore the outputs**: Review generated taxonomies in `outputs/`
3. **Iterate**: Try different keywords and parameters
4. **Stage 2**: Visualization generation (coming soon)

## Tips

- Start with smaller analyses (`--max-repos 20`) to test
- Use `--no-save-raw` to reduce storage if you don't need raw data
- Review example maps in `example-maps/` for inspiration
- The `_latest.json` files are useful for quick access to recent results
