import pandas as pd
import matplotlib.pyplot as plt

# Load vote and majority data
df_votes = pd.read_feather("votes_with_conformity.feather")
df_margins = pd.read_csv("congress_chamber_margins.csv")

# Filter and label votes
df = df_votes[
    (df_votes["congress"] >= 102) &
    (df_votes["party"].isin(["D", "R"])) &
    (~df_votes["vote"].isin(["Not Voting", "Present"]))
].copy()

# Map majority party
majority_lookup = df_margins.set_index(["congress", "chamber"])["majority_party"].to_dict()
df["majority_party"] = df.apply(
    lambda row: majority_lookup.get(
        (row["congress"], "House" if row["chamber"] == "h" else "Senate")
    ),
    axis=1
)
df["is_majority"] = df["party"] == df["majority_party"]

# Group and average
trend = df.groupby(["congress", "is_majority"]).agg(
    avg_entropy=("conforms_entropy", "mean")
).reset_index()

# Add start year for each Congress
trend["year"] = trend["congress"].apply(lambda c: 1789 + (c - 1) * 2)
trend["status"] = trend["is_majority"].map({True: "Majority", False: "Minority"})

# Pivot for plotting
pivot = trend.pivot(index="year", columns="status", values="avg_entropy")

# --- Plot ---
plt.figure(figsize=(10, 6))
plt.plot(pivot.index, pivot["Majority"], marker="o", label="Majority Party", color="steelblue")
plt.plot(pivot.index, pivot["Minority"], marker="o", label="Minority Party", color="darkorange")

plt.title("Entropy-Based Party Conformity Over Time (1991–2025)")
plt.xlabel("Year")
plt.ylabel("Average Entropy-Based Conformity")
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend()
plt.tight_layout()
plt.savefig("entropy_conformity_by_year.png")
plt.show()
