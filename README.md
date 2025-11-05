# GTM Intelligence Platform

## Overview

The platform automates:
1. **Data aggregation** — Collects Revolut-related signals (news, funding, partnerships, product launches, etc.).
2. **Categorization** — Classifies them into GTM themes such as *Product*, *Funding*, *Partnerships*, and more.
3. **Insight generation** — Creates concise summaries and actionable GTM recommendations.
4. **Automation** — Optionally posts daily updates to Slack via GitHub Actions.

---

## How It Works

### Collect
`fetch_signals.py` scrapes recent Revolut-related updates from Google News RSS feeds defined in `sources.yml`.

### Classify
`GTM_Intel.py`:
- Reads the fetched signals.
- Applies keyword rules from `category_rules.json`.
- Summarizes and ranks the signals by relevance.

### Notify
`slack_digest.py` sends a short daily summary to Slack (requires your webhook).
