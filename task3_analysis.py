import pandas as pd
import numpy as np

# load the cleaned csv from task 2
df = pd.read_csv("data/trends_clean.csv")
print(f"Loaded data: {df.shape}")

# print first 5 rows
print("\nFirst 5 rows:")
print(df.head())

# print average score and average comments
avg_score = df["score"].mean()
avg_comments = df["num_comments"].mean()
print(f"\nAverage score   : {avg_score:.3f}")
print(f"Average comments: {avg_comments:.3f}")

# numpy stats for score
print("\n--- NumPy Stats ---")
scores = np.array(df["score"])

print(f"Mean score   : {np.mean(scores):.3f}")
print(f"Median score : {np.median(scores):.3f}")
print(f"Std deviation: {np.std(scores):.3f}")
print(f"Max score    : {np.max(scores)}")
print(f"Min score    : {np.min(scores)}")

# which category has the most stories
top_category = df["category"].value_counts().idxmax()
top_count = df["category"].value_counts().max()
print(f"\nMost stories in: {top_category} ({top_count} stories)")

# which story has the most comments
most_commented = df.loc[df["num_comments"].idxmax()]
print(f"\nMost commented story: \"{most_commented['title']}\"  — {most_commented['num_comments']} comments")

# add engagement column
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# add is_popular column based on average score
df["is_popular"] = df["score"] > avg_score

# save updated dataframe to new csv
df.to_csv("data/trends_analysed.csv", index=False)
print("\nSaved to data/trends_analysed.csv")
