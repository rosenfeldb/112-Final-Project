import pandas as pd
import matplotlib.pyplot as plt

print("Loading vote data...")
df = pd.read_feather("votes_with_conformity.feather")

print("Filtering to valid D/R votes...")
df = df[
    df["party"].isin(["D", "R"]) &
    df["chamber"].isin(["h", "s"]) &
    ~df["vote"].isin(["Not Voting", "Present"])
].copy()

print("Calculating conformity by congress, party, and chamber...")
summary = df.groupby(["congress", "party", "chamber"]).agg(
    avg_simple=("conforms_simple", "mean"),
    n_votes=("vote", "count")
).reset_index()

# Convert congress to start year
summary["start_year"] = 1987 + 2 * (summary["congress"] - 101)

# Label mapping
chamber_labels = {"h": "House", "s": "Senate"}
color_map = {"D": "blue", "R": "red"}
linestyle_map = {"h": "-", "s": "--"}

print("Plotting...")
plt.figure(figsize=(10, 6))

for (party, chamber), group in summary.groupby(["party", "chamber"]):
    label = f"{party} - {chamber_labels[chamber]}"
    plt.plot(
        group["start_year"],
        group["avg_simple"],
        label=label,
        color=color_map[party],
        linestyle=linestyle_map[chamber],
        marker="o"
    )

plt.title("Party Conformity Over Time by Chamber (Simple Majority Match)")
plt.xlabel("Congress Start Year")
plt.ylabel("Average Conformity")
plt.ylim(0.7, 1.01)
plt.grid(True)
plt.legend(title="Party and Chamber")
plt.tight_layout()
plt.savefig("party_conformity_by_chamber.png")
plt.show()

print("Done! Plot saved as 'party_conformity_by_chamber.png'")
