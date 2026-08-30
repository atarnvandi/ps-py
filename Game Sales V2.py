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
# %%
# Exploratory Data Analysis

# 1. Most Selling Game
top_game_by_sales = df.groupby("title")["total_sales"].sum().nlargest(5)

# 2. Variable Comparison - Game by Console
top_game_by_console = (
    df.groupby(["title", "console"])["total_sales"].sum().nlargest(5).reset_index()
)

# 3. Variable Comparison - Console by Genre
top_console_by_genre = (
    df.groupby(["console", "genre"])["total_sales"].sum().nlargest(5).reset_index()
)
