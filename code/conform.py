import pandas as pd
import numpy as np
from scipy.stats import entropy

# Load your existing flattened vote dataset
df = pd.read_feather("all_votes.feather")

# Filter out non-votes if you want
df = df[~df["vote"].isin(["Not Voting", "Present"])].copy()

# GROUP 1: Party vote breakdown per vote_id
grouped = df.groupby(["vote_id", "party", "vote"]).size().reset_index(name="count")

# PARTY MAJORITY POSITION
# Find most common vote per party per bill
majority = (
    grouped.sort_values("count", ascending=False)
    .drop_duplicates(subset=["vote_id", "party"])
    .rename(columns={"vote": "party_majority_vote", "count": "majority_count"})
)

# Merge back into main df
df = df.merge(majority[["vote_id", "party", "party_majority_vote", "majority_count"]], 
              on=["vote_id", "party"], how="left")

# Count total party votes per vote
party_total = grouped.groupby(["vote_id", "party"])["count"].sum().reset_index(name="party_vote_total")
df = df.merge(party_total, on=["vote_id", "party"], how="left")

# Simple majority match
df["conforms_simple"] = df["vote"] == df["party_majority_vote"]

# Weighted confidence
df["conforms_weighted"] = np.where(
    df["conforms_simple"],
    df["majority_count"] / df["party_vote_total"],
    0.0
)

# Entropy-adjusted
# Compute entropy per party per vote_id
def compute_entropy(x):
    p = x["count"] / x["count"].sum()
    return entropy(p, base=2)

entropy_df = (
    grouped.groupby(["vote_id", "party"])
    .apply(compute_entropy)
    .reset_index(name="party_entropy")
)

df = df.merge(entropy_df, on=["vote_id", "party"], how="left")

df["conforms_entropy"] = np.where(
    df["conforms_simple"],
    1 - df["party_entropy"],
    0.0
)

# GROUP 2: Aggregate per member
member_scores = df.groupby(["member_id", "member_name", "party", "state"]).agg(
    votes_cast=("conforms_simple", "count"),
    pct_conform_simple=("conforms_simple", "mean"),
    pct_conform_weighted=("conforms_weighted", "mean"),
    pct_conform_entropy=("conforms_entropy", "mean")
).reset_index()

# Save for later
df.to_feather("votes_with_conformity.feather")
member_scores.to_feather("member_conformity_scores.feather")
