# Ecosystem Mapper

An experimental AI agent that automatically discovers, categorizes, and visualizes technology ecosystems based on keyword searches.

## Overview

Ecosystem Mapper takes a keyword (e.g., "agentic AI", "vector databases", "MLOps") and automatically:

1. **Discovers** recent projects and resources across GitHub and the web
2. **Analyzes** the landscape to create a taxonomy/categorization
3. **Identifies** representative examples within each category
4. **Generates** visual ecosystem maps showing the landscape

## Architecture

### Stage 1: Data Collection & Analysis

**Input:** User-provided keyword (e.g., "agentic AI")

**Data Sources:**
- **GitHub API**: Search for repositories created in the last 3 months matching the keyword
- **Tavily Search**: Web search to find articles, tools, and resources

**Analysis Engine:**
- **Model**: Google Gemini 3 Flash Preview (via OpenRouter)
- **Task**: Cross-analyze projects and resources to:
  - Create a taxonomy/categorization scheme
  - Identify main categories within the ecosystem
  - Find representative examples for each category
  - Determine relationships and groupings

**Output:** Structured taxonomy with categorized examples

### Stage 2: Visualization Generation

**Input:** Taxonomy and categorized examples from Stage 1

**Process:**
- Use example ecosystem maps as style references
- Generate visual representations of the ecosystem
- Create market map-style visualizations showing:
  - Categories and subcategories
  - Representative projects/companies
  - Relationships and groupings

**Output:** Ecosystem map images

## Example Use Cases

```bash
# Analyze the agentic AI ecosystem
python agent.py --keyword "agentic AI"

# Explore vector database landscape
python agent.py --keyword "vector databases"

# Map out the RAG (Retrieval Augmented Generation) ecosystem
python agent.py --keyword "RAG frameworks"
```

## Configuration

Set up your `.env` file (see `.env.example`):

```env
# OpenRouter Configuration
OR_RESEARCH_MODEL_NAME=google/gemini-3-flash-preview
OR_IMAGE_GEN_MODEL_NAME_1=google/gemini-3-pro-image-preview
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Tavily Search API
TAVILY_API_KEY=your_tavily_api_key_here

# GitHub Personal Access Token
GITHUB_PAT=your_github_personal_access_token_here
```

## Project Structure

```
Ecosystem-Mapper/
├── agent.py                 # Main orchestration script
├── modules/
│   ├── github_collector.py  # GitHub API integration
│   ├── tavily_search.py     # Tavily search integration
│   ├── taxonomy_analyzer.py # Gemini-powered taxonomy creation
│   └── visualizer.py        # Map generation (Stage 2)
├── example-maps/            # Reference ecosystem maps
├── outputs/                 # Generated taxonomies and maps
└── README.md
```

## Dependencies

- Python 3.10+
- OpenRouter API access (for Gemini)
- GitHub API token
- Tavily API key
- Required packages: `requests`, `python-dotenv`, `openai` (for OpenRouter)

## Development Status

- ✅ **Stage 1a**: Data collection modules (GitHub + Tavily)
- ✅ **Stage 1b**: Taxonomy analysis with Gemini
- 🚧 **Stage 2**: Visualization generation (planned)

## Reference Examples

The `example-maps/` folder contains ecosystem maps from public sources that serve as visual style references for the maps we'll generate.

## License

Private repository - Daniel Rosehill

## Notes

This is an experimental project exploring automated ecosystem mapping and visualization. The agent uses AI to understand domain landscapes and create structured categorizations automatically.
