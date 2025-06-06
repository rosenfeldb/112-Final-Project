import pandas as pd
import matplotlib.pyplot as plt

# Load your data
df_votes = pd.read_feather("votes_with_conformity.feather")
df_margins = pd.read_csv("congress_chamber_margins.csv")

# Filter votes
df = df_votes[
    (df_votes["congress"] >= 102) &
    (df_votes["party"].isin(["D", "R"])) &
    (~df_votes["vote"].isin(["Not Voting", "Present"]))
].copy()

# Compute avg entropy conformity by congress/chamber
entropy_by_congress = df.groupby(["congress", "chamber"]).agg(
    avg_entropy=("conforms_entropy", "mean")
).reset_index()

# Normalize chamber names for merging
df_margins["chamber_code"] = df_margins["chamber"].map({"House": "h", "Senate": "s"})
df_margins["abs_margin"] = df_margins["margin"].abs()

# Merge data
merged = entropy_by_congress.merge(
    df_margins[["congress", "chamber_code", "abs_margin"]],
    left_on=["congress", "chamber"],
    right_on=["congress", "chamber_code"],
    how="inner"
)

# Plot
plt.figure(figsize=(10, 6))
for chamber_code, label, color in zip(["h", "s"], ["House", "Senate"], ["steelblue", "darkred"]):
    subset = merged[merged["chamber"] == chamber_code]
    plt.scatter(
        subset["abs_margin"],
        subset["avg_entropy"],
        label=label,
        color=color,
        alpha=0.7,
        edgecolor="black"
    )

plt.xlabel("Absolute Seat Margin")
plt.ylabel("Average Entropy-Based Conformity")
plt.title("Conformity vs. Seat Margin by Chamber (102nd–119th Congress)")
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig("conformity_vs_margin_scatter_fixed.png")
plt.show()
