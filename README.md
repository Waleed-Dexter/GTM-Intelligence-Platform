# GTM Intelligence Platform (Task 2 – Revolut Global)

A lightweight prototype that gathers external **market signals** for **Revolut (Global)** and translates them into **actionable GTM insights**.  
Built as part of the **Wavess Internship Project – Task 2**.

---

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
`GTM_Intel_Task2.py`:
- Reads the fetched signals.
- Applies keyword rules from `category_rules.json`.
- Summarizes and ranks the signals by relevance.

### Notify
`slack_digest.py` sends a short daily summary to Slack (requires your webhook).

---

## Folder Structure

├── fetch_signals.py # Collects Revolut-related news
├── GTM_Intel_Task2.py # Classifies & summarizes signals
├── slack_digest.py # Posts Slack digest via webhook
├── sources.yml # Feed URLs and keyword filters
├── category_rules.json # GTM classification rules
├── icp_profile.json # ICP configuration
├── signals_template.csv # Placeholder (auto-filled by fetch_signals)
├── requirements.txt # Dependencies
├── out/ # Output folder (auto-created)
└── gtm-intel-daily.yml # CI automation (runs daily + manual trigger)
