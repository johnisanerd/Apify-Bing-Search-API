"""
Bing Search API: A Quick Start Example
See more at: https://apify.com/johnvc/bing-search-api?fpr=9n7kx3
Input schema: https://apify.com/johnvc/bing-search-api/input-schema?fpr=9n7kx3

This script shows how to call the Bing Search API on Apify from Python and
read its structured JSON output. The default run stays deliberately small so
your first call is inexpensive; the --example recipes mirror the API's main
use cases (see the README Recipes section).

Get your free Apify API key at: https://apify.com?fpr=9n7kx3

Examples:
  uv run python bing-search-api-example.py
  uv run python bing-search-api-example.py --example rank_tracking
"""

from __future__ import annotations

import argparse
import os
from typing import Any

from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

ACTOR_ID = "johnvc/bing-search-api"


def _print_items(items: list[dict[str, Any]]) -> None:
    """Print a short summary of dataset items."""
    print(f"Returned {len(items)} item(s).\n")
    for item in items:
        print(item.get('position'), item.get('title'), item.get('url'))


def run_default(client: ApifyClient) -> None:
    """Cheap general quick-start. Inputs stay small on purpose."""
    run_input: dict[str, Any] = {
        "query": "web scraping tools",
        "max_pages": 1,  # one page on purpose; the page is also the billing unit
    }
    run = client.actor(ACTOR_ID).call(run_input=run_input)
    if run is None:
        raise SystemExit("The Actor run did not return a result.")
    items = list(client.dataset(run.default_dataset_id).iterate_items())
    _print_items(items)


def run_rank_tracking(client: ApifyClient) -> None:
    """One rank-tracking snapshot (mirrors the bing-rank-tracking use case).

    Schedule this with your own keyword and market; position plus page combine
    into an absolute rank per run.
    """
    run_input: dict[str, Any] = {
        "query": "web scraping tools",
        "max_pages": 1,
        "location": "Seattle, Washington",
        "device": "desktop",
    }
    run = client.actor(ACTOR_ID).call(run_input=run_input)
    if run is None:
        raise SystemExit("The Actor run did not return a result.")
    for item in client.dataset(run.default_dataset_id).iterate_items():
        print(f"p{item.get('page')}#{item.get('position'):>2} {item.get('title', '')[:70]}")


def run_serp_with_ads(client: ApifyClient) -> None:
    """A page with ad placements included, for competitor ad monitoring."""
    run_input: dict[str, Any] = {
        "query": "best crm software",
        "max_pages": 1,
        "include_ads": True,
    }
    run = client.actor(ACTOR_ID).call(run_input=run_input)
    if run is None:
        raise SystemExit("The Actor run did not return a result.")
    items = list(client.dataset(run.default_dataset_id).iterate_items())
    _print_items(items)


def main() -> None:
    """Dispatch a quick-start or use-case recipe."""
    parser = argparse.ArgumentParser(description="Bing Search API examples")
    parser.add_argument(
        "--example",
        default="default",
        choices=['default', 'rank_tracking', 'serp_with_ads'],
        help="Which recipe to run (see README Recipes).",
    )
    args = parser.parse_args()

    token = os.getenv("APIFY_API_TOKEN")
    if not token:
        raise SystemExit("Set APIFY_API_TOKEN in .env or the environment.")

    client = ApifyClient(token)
    dispatch = {
        "default": run_default,
        "rank_tracking": run_rank_tracking,
        "serp_with_ads": run_serp_with_ads,
    }
    dispatch[args.example](client)


if __name__ == "__main__":
    main()
