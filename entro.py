import pandas as pd
import matplotlib.pyplot as plt

print("Loading vote data with conformity scores...")
df = pd.read_feather("votes_with_conformity.feather")

print("Filtering to Democrats and Republicans with valid votes...")
df = df[
    df["party"].isin(["D", "R"]) &
    ~df["vote"].isin(["Not Voting", "Present"])
].copy()

print("Grouping by congress and party...")
summary = df.groupby(["congress", "party"]).agg(
    avg_simple=("conforms_simple", "mean"),
    avg_entropy=("conforms_entropy", "mean"),
    n_votes=("vote", "count")
).reset_index()

# Convert Congress number to starting year
summary["start_year"] = 1987 + 2 * (summary["congress"] - 101)
summary["gap"] = summary["avg_simple"] - summary["avg_entropy"]

print("Plotting conformity and entropy-adjusted conformity...")
plt.figure(figsize=(10, 6))

colors = {"D": "blue", "R": "red"}
for party in ["D", "R"]:
    subset = summary[summary["party"] == party]
    plt.plot(
        subset["start_year"], subset["avg_entropy"],
        marker="x", label=f"{party} - Entropy Adj.", color=colors[party], linestyle="--"
    )

plt.title("Party Conformity vs. Entropy-Adjusted Conformity (Over Time)")
plt.xlabel("Congress Start Year")
plt.ylabel("Average Conformity")
plt.grid(True)
plt.legend(title="Party")
plt.tight_layout()
plt.savefig("party_conformity_vs_entropy.png")
plt.show()

print("Done! Plot saved as 'party_conformity_vs_entropy.png'")
