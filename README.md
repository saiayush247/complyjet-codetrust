# CodeTrust

A small tool that flags GitHub pull requests merged with no verified human review — built as a proof-of-concept for a SOC 2 CC8.1 (Change Management) evidence signal.

## What it does

`detective.py` scans a repo's merged PRs. For each one, it checks two things:
1. How fast it was merged after being opened
2. Whether it has any GitHub reviews or comments

If a PR merged in under 2 minutes **and** has zero reviews or comments, it writes a JSON evidence record flagging it as "review depth unverified." Everything else is left alone.

`app.py` is a live Flask dashboard showing the same check for the most recent PR.

## Why this check, specifically

Fast, uncommented merges are a real gap in change management controls — there's no evidence a second person looked at the change before it shipped. This tool only reports what it can verify directly from GitHub's API (merge timing, review count, comment count). It does not attempt to detect AI-generated code or make claims it can't back with data.

## Scope

This is a proof-of-concept against a single hardcoded repo, not a production integration. No auth flow, no multi-tenant support, no persistence beyond local JSON files. Built to demonstrate the detection logic and evidence format, not to be dropped into a real compliance pipeline as-is.

## Running it

```bash
export GITHUB_TOKEN="your_token"   # unauthenticated calls are rate-limited to 60/hr
python detective.py                 # scans and writes evidence_pr_*.json
python app.py                       # runs the live dashboard on :5000
```

## Example evidence output

See `evidence_pr_2.json` for a real flagged finding from this repo's own PR history.
