import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv("member_conformity_over_time.csv")

# Filter for Nancy Pelosi (case-insensitive match)
pelosi = df[df["member_name"].str.contains("Pelosi", case=False)]

# Plot her conformity over time
plt.figure(figsize=(10, 5))
plt.plot(pelosi["congress"], pelosi["avg_entropy_conformity"], marker="o", label="Entropy-Based")
plt.plot(pelosi["congress"], pelosi["avg_simple_conformity"], marker="x", linestyle="--", label="Simple")

plt.title("Nancy Pelosi: Party Conformity Over Time")
plt.xlabel("Congress")
plt.ylabel("Conformity Score")
plt.ylim(0.4, 1.1)
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend()
plt.tight_layout()
plt.savefig("pelosi_conformity_over_time.png")
plt.show()
