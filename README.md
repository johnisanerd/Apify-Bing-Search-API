# 📊 Bing Search API: Bing rank tracking and SERP data as JSON

Actor: [johnvc/bing-search-api](https://apify.com/johnvc/bing-search-api?fpr=9n7kx3) · [Input schema](https://apify.com/johnvc/bing-search-api/input-schema?fpr=9n7kx3)

This repo shows two ways to use the [Bing Search API](https://apify.com/johnvc/bing-search-api?fpr=9n7kx3) on Apify: a Python quick start and MCP installs for five AI clients. Query Bing, get organic results with real destination URLs, optionally the ads, and track where a domain ranks by city and device. If you were about to scrape Bing search results yourself, this is the page as JSON with the redirect wrappers already unwound.

## Video Walkthrough

[![Watch the walkthrough](https://img.youtube.com/vi/jREWahDGhJM/maxresdefault.jpg)](https://www.youtube.com/watch?v=jREWahDGhJM)

### Text walkthrough

The bing search api takes a query plus max_pages, which is also the billing unit: you pay per page of results, whatever that page holds, because the engine controls its own depth. Each organic row carries position, page, title, snippet, the real url rather than an expiring tracking link, displayedUrl and date. Set location to a city and device to desktop or mobile for bing rank tracking, the rank_tracking recipe in this repo; combine page and position for an absolute rank. Switch include_ads on and the paid placements come back too, marked as ads, at no extra charge.

## Quick Start

You need Python 3.11+ and a free Apify API key: sign up at [apify.com](https://apify.com?fpr=9n7kx3), then copy your token from Console Settings.

```bash
git clone https://github.com/johnisanerd/Apify-Bing-Search-API.git
cd Apify-Bing-Search-API
uv sync
cp .env.example .env   # then paste your APIFY_API_TOKEN
uv run python bing-search-api-example.py
```

Run a specific recipe:

```bash
uv run python bing-search-api-example.py --example rank_tracking
```

## Why use this API

- Organic results with the real destination URL, not an expiring redirect wrapper
- position plus page combine into an absolute rank for tracking
- Ad placements included free when you want competitor ad monitoring
- City-level location and device targeting for local and mobile rank checks
- Bing operators pass straight through: site:, filetype:, OR, NOT

## Recipes

The example script ships ready-made recipes that mirror this API's main use cases:

- **Bing rank tracking** (`--example rank_tracking`): Runs one query with a city and device and prints ranked results; schedule it for a rank history.
- **SERP with ad placements** (`--example serp_with_ads`): Pulls a page with ads included for competitor ad monitoring.

**Schedule tip:** save any of these inputs as a task in the [Apify Console](https://apify.com/johnvc/bing-search-api?fpr=9n7kx3) and attach a schedule. A daily or weekly run turns a one-off pull into a pipeline with zero manual work.

## Usage Examples

Basic input:

```json
{
  "query": "project management software",
  "max_pages": 1
}
```

Advanced input:

```json
{
  "query": "coffee shops",
  "max_pages": 2,
  "location": "Seattle, Washington",
  "device": "mobile",
  "include_ads": true
}
```

## Input Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `query` | string | yes | none | REQUIRED. |
| `max_pages` | integer | no | `1` | How many pages of results to fetch. |
| `include_ads` | boolean | no | `false` | Also return the paid placements on each page, marked with resultType 'ad'. |
| `country` | string | no | none | Optional two letter country code such as us, gb or de. |
| `market` | string | no | none | Optional language and country pair such as en-US or de-DE. |
| `location` | string | no | none | Optional city to search from, such as 'Seattle, Washington'. |
| `safe_search` | string | no | `"Moderate"` | Optional adult content filter. |
| `device` | string | no | `"desktop"` | Optional device to emulate. |

## Output Format

One row from a real run:

```json
{
  "resultType": "organic",
  "query": "project management software",
  "page": 1,
  "position": 1,
  "title": "Best Project Management Software Compared For 2026",
  "snippet": "A side by side comparison of the leading project management platforms.",
  "url": "https://example.com/blog/project-management-software/",
  "displayedUrl": "https://example.com",
  "date": "Apr 13, 2026"
}
```

## n8n integration

Available as an n8n community node, **[n8n-nodes-bing-search-api](https://www.npmjs.com/package/n8n-nodes-bing-search-api)**. In n8n: Settings, Community Nodes, install `n8n-nodes-bing-search-api`, then use it in any workflow (it also works as an AI Agent tool).

## People also search for

### Is this a Bing scraper?

Use it wherever you would scrape Bing search results, but it returns the page as JSON in one call, with the redirect wrappers replaced by real destination URLs.

### How do I track Bing rankings for my site?

Run the rank_tracking recipe on a schedule with your keyword, city and device, and store position and page per run. The series is your rank history.

### Why per page instead of per result?

Bing gives no page-size control and organic depth swings between 2 and 10 results per page. Per-page billing means a thin page never costs more than it is worth.

### Can I see the ads too?

Yes, set include_ads to true. They are on the page you already paid for, so including them costs nothing extra.

## Install in Claude Cowork Desktop

![Install in Claude Cowork Desktop](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_desktop.png)

Cowork is the desktop app's automation mode. To give it the Bing Search API as a tool, add the Apify MCP server as a connector.

1. Open the Claude desktop app and go to **Settings -> Connectors** (or **Settings -> Developer -> Edit Config** to edit `claude_desktop_config.json` directly).
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
2. Add the Apify MCP server, preloaded with only this Actor:

```json
{
  "mcpServers": {
    "apify": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.apify.com/?tools=actors,docs,johnvc/bing-search-api"
      ]
    }
  }
}
```

3. Restart the app. When Cowork first calls the tool, complete the OAuth prompt in your browser, or add your Apify API token in the connector settings to skip OAuth.
4. In a Cowork chat, confirm the tool is available and ask it to run the Bing Search API.

Download the desktop app and start a free trial: https://claude.ai/referral/uIlpa7nPLg
More help: https://docs.apify.com/platform/integrations/claude-desktop

## Install in Claude Code

![Install in Claude Code](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_code.png)

Claude Code is the command-line tool. Add the Actor's MCP server with one command:

```bash
claude mcp add --transport http apify \
  "https://mcp.apify.com/?tools=actors,docs,johnvc/bing-search-api"
```

To use a token instead of browser OAuth:

```bash
claude mcp add --transport http apify \
  "https://mcp.apify.com/?tools=actors,docs,johnvc/bing-search-api" \
  --header "Authorization: Bearer YOUR_APIFY_TOKEN"
```

Then verify with `claude mcp list`, or run `/mcp` inside a session. Ask Claude Code to call the Bing Search API.

Try Claude Code free: https://claude.ai/referral/uIlpa7nPLg
Claude Code MCP docs: https://code.claude.com/docs/en/mcp

## Install in Claude (website)

![Install in Claude (website)](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_ai.png)

On claude.ai you add Apify as a connector, then enable just this Actor's tool.

1. Go to **Settings -> Connectors -> Browse connectors** and search for **Apify MCP server**. Install it (enable or update if prompted).
2. When connecting, authenticate with your Apify API token, and enable the tool `johnvc/bing-search-api`.
3. In any chat, open **+ -> Connectors** and turn on **Apify**.
4. Alternatively, choose **Add custom connector** and paste the full MCP URL `https://mcp.apify.com/?tools=actors,docs,johnvc/bing-search-api`, using OAuth when prompted.
5. Ask Claude to run the Bing Search API.

Open Claude on the web: https://claude.ai

## Install in Cursor

![Install in Cursor](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_cursor.png)

Cursor reads MCP servers from a project file at `.cursor/mcp.json`.

1. In your project, create `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com/?tools=actors,docs,johnvc/bing-search-api"
    }
  }
}
```

2. If you prefer token auth over browser OAuth, add a header:

```json
{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com/?tools=actors,docs,johnvc/bing-search-api",
      "headers": { "Authorization": "Bearer YOUR_APIFY_TOKEN" }
    }
  }
}
```

3. Open **Cursor -> Settings -> MCP** and confirm the **apify** server is connected (green dot).
4. In Composer or Chat, ask Cursor to call the Bing Search API.

New to Cursor? Get it here: https://cursor.com/referral?code=XQP4VBLI3NNX

## Install in ChatGPT

![Install in ChatGPT](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_ChatGPT.png)

ChatGPT connects to the Apify MCP server through Developer mode (available on ChatGPT Pro, Plus, Business, Enterprise, and Education plans).

1. Click your profile icon, then go to **Settings > Apps**. If you do not see a **Create app** button, open **Advanced settings** and enable **Developer mode**.
2. Click **Create app** and fill out the form:
   - **Name:** Apify
   - **MCP Server URL:** `https://mcp.apify.com/?tools=actors,docs,johnvc/bing-search-api`
   - **Authentication:** OAuth
3. Click **Create** and authorize the connection with Apify.
4. To use the app in a conversation, click **+** in the chat, choose **Developer mode**, and select **Apify**.

More help: https://docs.apify.com/platform/integrations/mcp


---

Made with care by [johnvc on Apify](https://apify.com/johnvc?fpr=9n7kx3). This example repo is part of [Alpha OSINT](https://www.alphaosint.com), toolset of financial and operations data sources and APIs.

Last Updated: 2026.08.18
