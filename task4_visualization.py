import pandas as pd
import matplotlib.pyplot as plt
import os

# load the analysed csv from task 3
df = pd.read_csv("data/trends_analysed.csv")

# create outputs folder if it doesnt exist
if not os.path.exists("outputs"):
    os.makedirs("outputs")

# ── Chart 1: Top 10 Stories by Score ──────────────────────────────────────────

# sort by score and grab top 10
top10 = df.sort_values("score", ascending=False).head(10)

# shorten titles longer than 50 characters
top10 = top10.copy()
top10["short_title"] = top10["title"].apply(lambda x: x[:50] + "..." if len(x) > 50 else x)

plt.figure(figsize=(10, 6))
plt.barh(top10["short_title"], top10["score"], color="steelblue")
plt.xlabel("Score")
plt.ylabel("Story Title")
plt.title("Top 10 Stories by Score")
plt.tight_layout()
plt.savefig("outputs/chart1_top_stories.png")
plt.show()

# ── Chart 2: Stories per Category ─────────────────────────────────────────────

# count stories per category
category_counts = df["category"].value_counts()

# different color for each bar
colors = ["steelblue", "orange", "green", "red", "purple"]

plt.figure(figsize=(8, 5))
plt.bar(category_counts.index, category_counts.values, color=colors)
plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.title("Stories per Category")
plt.tight_layout()
plt.savefig("outputs/chart2_categories.png")
plt.show()

# ── Chart 3: Score vs Comments ─────────────────────────────────────────────────

# split into popular and not popular using is_popular column
popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

plt.figure(figsize=(8, 5))
plt.scatter(not_popular["score"], not_popular["num_comments"], color="blue", label="not popular", alpha=0.6)
plt.scatter(popular["score"], popular["num_comments"], color="red", label="popular", alpha=0.6)
plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.title("Score vs Comments")
plt.legend()
plt.tight_layout()
plt.savefig("outputs/chart3_scatter.png")
plt.show()

# ── Bonus Dashboard ────────────────────────────────────────────────────────────

fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle("TrendPulse Dashboard")

# chart 1 in dashboard
axes[0].barh(top10["short_title"], top10["score"], color="steelblue")
axes[0].set_title("Top 10 Stories by Score")
axes[0].set_xlabel("Score")

# chart 2 in dashboard
axes[1].bar(category_counts.index, category_counts.values, color=colors)
axes[1].set_title("Stories per Category")
axes[1].set_xlabel("Category")
axes[1].set_ylabel("Number of Stories")

# chart 3 in dashboard
axes[2].scatter(not_popular["score"], not_popular["num_comments"], color="blue", label="not popular", alpha=0.6)
axes[2].scatter(popular["score"], popular["num_comments"], color="red", label="popular", alpha=0.6)
axes[2].set_title("Score vs Comments")
axes[2].set_xlabel("Score")
axes[2].set_ylabel("Number of Comments")
axes[2].legend()

plt.tight_layout()
plt.savefig("outputs/dashboard.png")
plt.show()
