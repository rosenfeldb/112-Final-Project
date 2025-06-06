import pandas as pd
import matplotlib.pyplot as plt

print("Loading vote data with conformity scores...")
df = pd.read_feather("votes_with_conformity.feather")

print("Filtering to D and R only, and valid votes...")
df = df[
    df["party"].isin(["D", "R"]) & 
    ~df["vote"].isin(["Not Voting", "Present"])
].copy()

print("Computing conformity over time by party and congress...")
congress_party = df.groupby(["congress", "party"]).agg(
    avg_simple=("conforms_simple", "mean"),
    n_votes=("vote", "count")
).reset_index()

# Convert Congress number to starting year
# Congress 101 = 1989, Congress 102 = 1991, etc.
congress_party["start_year"] = 1987 + 2 * (congress_party["congress"] - 101)

print("Plotting...")
plt.figure(figsize=(10, 6))

party_colors = {"D": "blue", "R": "red"}
for party in ["D", "R"]:
    subset = congress_party[congress_party["party"] == party]
    plt.plot(
        subset["start_year"],
        subset["avg_simple"],
        marker="o",
        label=f"{party}",
        color=party_colors[party]
    )

plt.title("Party Conformity Over Time (Simple Majority Match)")
plt.xlabel("Congress Start Year")
plt.ylabel("Average Conformity")
plt.ylim(0.7, 1.01)
plt.grid(True)
plt.legend(title="Party")
plt.tight_layout()
plt.savefig("party_conformity_red_blue.png")
plt.show()

print("Done! Plot saved as 'party_conformity_red_blue.png'")
