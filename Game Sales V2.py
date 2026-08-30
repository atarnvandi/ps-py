# %% Importing Libraries
import pandas as pd

# %% Importing Data
raw_df = pd.read_csv("vgchartz-2024.csv")

# %% Check Point
df = raw_df.copy().drop(columns=["img", "last_update"])

# Data Cleaning
df["developer"] = df["developer"].fillna("Unknown")  # Empty Dev to 'Unknown'

to_fill = ["total_sales", "na_sales", "jp_sales", "pal_sales", "other_sales"]
df[to_fill] = df[to_fill].fillna(0)  # NaN Sales (int) to 0

df["release_date"] = pd.to_datetime(
    df["release_date"], errors="coerce"
)  # str to datetime
