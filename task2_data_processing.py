import pandas as pd
import os
import glob

# find the json file in data folder
files = glob.glob("data/trends_*.json")

if not files:
    print("no json file found in data folder")
else:
    # grab the first file found
    json_file = files[0]

    # load json file into a dataframe
    df = pd.read_json(json_file)
    print(f"Loaded {len(df)} stories from {json_file}")

    # remove duplicate stories with same post_id
    df = df.drop_duplicates(subset="post_id")
    print(f"After removing duplicates: {len(df)}")

    # drop rows where post_id, title or score is missing
    df = df.dropna(subset=["post_id", "title", "score"])
    print(f"After removing nulls: {len(df)}")

    # make sure score and num_comments are integers
    df["score"] = df["score"].astype(int)
    df["num_comments"] = df["num_comments"].astype(int)

    # remove stories where score is less than 5
    df = df[df["score"] >= 5]
    print(f"After removing low scores: {len(df)}")

    # strip extra spaces from title column
    df["title"] = df["title"].str.strip()

    # save cleaned data to csv file
    df.to_csv("data/trends_clean.csv", index=False)
    print(f"\nSaved {len(df)} rows to data/trends_clean.csv")

    # print how many stories per category
    print("\nStories per category:")
    print(df["category"].value_counts().to_string())
