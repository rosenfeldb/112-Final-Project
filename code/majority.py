import json
from pathlib import Path
import pandas as pd

# Adjust this path to your actual folder
base_path = Path("/Users/ben/Downloads/congress-main/data")

results = []

# Loop over Congress folders
for congress_folder in sorted(base_path.glob("*")):
    if not congress_folder.is_dir():
        continue

    congress_num = int(congress_folder.name)
    if congress_num < 102:
        continue

    # Separate for House and Senate
    for chamber in ["h", "s"]:
        vote_files = sorted((congress_folder / "votes").rglob(f"{chamber}*/data.json"))
        if not vote_files:
            continue

        # Load first available vote file
        try:
            with open(vote_files[0], "r") as f:
                vote_data = json.load(f)
        except Exception as e:
            print(f"Skipping {vote_files[0]} due to error: {e}")
            continue

        # Count party votes
        counts = {"R": 0, "D": 0}
        for category in vote_data.get("votes", {}).values():
            for voter in category:
                party = voter.get("party")
                if party in counts:
                    counts[party] += 1

        total = counts["R"] + counts["D"]
        margin = abs(counts["R"] - counts["D"])
        majority = "R" if counts["R"] > counts["D"] else "D"

        results.append({
            "congress": congress_num,
            "chamber": "House" if chamber == "h" else "Senate",
            "republicans": counts["R"],
            "democrats": counts["D"],
            "total_votes": total,
            "margin": margin,
            "majority_party": majority
        })

# Create and display DataFrame
df_chamber_margins = pd.DataFrame(results).sort_values(["congress", "chamber"])
df_chamber_margins.to_csv("congress_chamber_margins.csv", index=False)
print(df_chamber_margins)
