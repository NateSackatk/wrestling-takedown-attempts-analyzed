"""
Wrestling Match Analytics (v2)
--------------------------------
Reads matches.csv and takedown_attempts.csv, merges them, and reports
takedown success rate by technique (filtered to techniques with enough
attempts to mean something), success rate by period, and weight-cut
correlation.

Run:  python analyze_v2.py
"""

import pandas as pd
import matplotlib.pyplot as plt

# ---------- Config ----------
MIN_ATTEMPTS = 5  # techniques with fewer attempts than this are excluded
                   # from the "success rate by technique" chart/table --
                   # a technique you've tried once or twice doesn't have
                   # a meaningful success rate yet.

SUCCESS_OUTCOMES = {"scored_clean", "scored_scramble"}

# ---------- 1. Load ----------
matches = pd.read_csv("matches.csv")
attempts = pd.read_csv("takedown_attempts.csv")

# Clean weight_cut_lbs in case it has units baked in (e.g. "3_lbs")
if matches["weight_cut_lbs"].dtype == object:
    matches["weight_cut_lbs"] = (
        matches["weight_cut_lbs"].astype(str).str.extract(r"([\d.]+)").astype(float)
    )

print(f"Loaded {len(matches)} matches and {len(attempts)} takedown attempts.\n")

attempts["scored"] = attempts["outcome"].isin(SUCCESS_OUTCOMES)

# ---------- 2. Success rate by technique (filtered) ----------
by_technique = (
    attempts.groupby("technique")["scored"]
    .agg(attempts="count", successes="sum")
)
by_technique["success_rate"] = (by_technique["successes"] / by_technique["attempts"] * 100).round(1)

low_sample = by_technique[by_technique["attempts"] < MIN_ATTEMPTS]
by_technique_filtered = by_technique[by_technique["attempts"] >= MIN_ATTEMPTS].sort_values(
    "success_rate", ascending=True  # ascending so horizontal bar chart reads top-to-bottom nicely
)

print(f"=== Takedown Success Rate by Technique (min {MIN_ATTEMPTS} attempts) ===")
print(by_technique_filtered.sort_values("success_rate", ascending=False))
print(f"\n({len(low_sample)} techniques excluded for having fewer than {MIN_ATTEMPTS} attempts: "
      f"{', '.join(low_sample.index)})\n")

# ---------- 3. Success rate by period ----------
by_period = (
    attempts.groupby("period")["scored"]
    .agg(attempts="count", successes="sum")
)
by_period["success_rate"] = (by_period["successes"] / by_period["attempts"] * 100).round(1)

print("=== Takedown Success Rate by Period ===")
print(by_period)
print()

# ---------- 4. Weight cut vs. result ----------
match_success = (
    attempts.groupby("match_id")["scored"]
    .mean()
    .mul(100)
    .round(1)
    .rename("takedown_success_rate")
)
merged = matches.merge(match_success, on="match_id", how="left")

if merged["weight_cut_lbs"].notna().sum() > 1:
    corr = merged["weight_cut_lbs"].corr(merged["takedown_success_rate"])
    print(f"Correlation between weight cut (lbs) and takedown success rate: {corr:.2f}")
    print("(Closer to -1 = bigger cuts linked to worse takedown performance;")
    print(" closer to +1 = bigger cuts linked to better performance; near 0 = no clear link)\n")

# ---------- 5. Charts ----------
fig, axes = plt.subplots(1, 2, figsize=(13, max(5, len(by_technique_filtered) * 0.35)))

# Horizontal bar chart -- much more readable with many technique names
axes[0].barh(by_technique_filtered.index, by_technique_filtered["success_rate"], color="#2b6cb0")
axes[0].set_title(f"Takedown Success Rate by Technique (min {MIN_ATTEMPTS} attempts)")
axes[0].set_xlabel("Success Rate (%)")
axes[0].set_xlim(0, 100)

by_period["success_rate"].plot(kind="bar", ax=axes[1], color="#2f855a")
axes[1].set_title("Takedown Success Rate by Period")
axes[1].set_ylabel("Success Rate (%)")
axes[1].set_xlabel("Period")
axes[1].set_ylim(0, 100)
axes[1].tick_params(axis="x", rotation=0)

plt.tight_layout()
plt.savefig("wrestling_stats.png", dpi=150)
print("Saved charts to wrestling_stats.png")
plt.show()
