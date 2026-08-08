# wrestling-takedown-attempts-analyzed
An effective way of analyzing takedown success rates by technique, match period, and weight cut across my competitive wrestling matches.
# Wrestling Match Analytics

Analyzes takedown success rates by technique, match period, and weight cut across my competitive wrestling matches this past season.

## Background

I logged 21 matches, tracking match-level info (opponent, tournament, weight cut, result) and every individual takedown attempt (112 of them) within each match (technique used, period, and outcome). This script analyzes that data to find patterns in my own performance.

## How to run it

1. Install dependencies: `pip install pandas matplotlib`
2. Make sure `matches.csv` and `takedown_attempts.csv` are in the same folder as `analyze_v2.py`
3. Run: `python analyze_v2.py`

The script prints summary tables to the console and saves a chart (`wrestling_stats.png`).

## Findings

- **Takedown success drops sharply in the 2nd period** — 66.0% in period 1, 44.7% in period 2, back up to 60.0% in period 3. Worth digging into whether this is fatigue, opponent adjustment after seeing my period-1 shot, or a strategy shift on my end.
- **Most reliable techniques** (minimum 4 attempts logged): elbow slide-by (61.3% success across 31 attempts, my most-used shot), misdirection single (75.0%), knee pull single (75.0%).
- **No meaningful correlation between weight cut size and takedown success rate** (correlation ≈ -0.08) — bigger cuts didn't measurably hurt or help my performance in this sample. Consider opponent skill level.

## Data

- `matches.csv` — one row per match (date, tournament, weight class, weight cut, opponent, result)
- `takedown_attempts.csv` — one row per takedown attempt (linked to match by `match_id`, includes technique, period, and outcome)
