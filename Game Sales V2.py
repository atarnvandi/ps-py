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
top_game_by_sales = (
    df.groupby("title")["total_sales"]
    .sum()
    .to_frame()
    .nlargest(5, columns="total_sales")
    .reset_index()
)

# 2. Most Selling Genre
top_genre_by_sales = (
    df.groupby("genre")["total_sales"]
    .sum()
    .to_frame()
    .nlargest(5, columns="total_sales")
    .reset_index()
)

# 3. Variable Comparison - Game Sales by Console
top_game_console_by_sales = (
    df.groupby(["title", "console"])["total_sales"].sum().nlargest(5).reset_index()
)

# 4. Variable Comparison - Genre Sales by Console
top_console_genre_by_sales = (
    df.groupby(["console", "genre"])["total_sales"].sum().nlargest(5).reset_index()
)

# There top 5 Genre are Sports, Action, Shooter, Misc, and Racing. As the wide variable after Consoles.

# 5. How's GTA V From Action/ Action-Adventure Bocome The Most Selling Game When The Top Genre is Sports
## Sports Game Title Sales
sports_titles_by_sales = (
    df[df["genre"] == "Sports"]
    .groupby("title")["total_sales"]
    .sum()
    .reset_index()
    .rename(columns={"total_sales": "sport_sales"})
)
## Sports Game Genre On Consoles
sports_console_by_sales = (
    df[df["genre"] == "Sports"]
    .groupby("console")["total_sales"]
    .sum()
    .nlargest(5)
    .reset_index()
    .rename(columns={"total_sales": "sport_sales"})
)
## Sports Game Titles On Console
sports_titles_by_sales = (
    df[df["genre"] == "Sports"]
    .groupby("title")["total_sales"]
    .sum()
    .reset_index()
    .rename(columns={"total_sales": "sport_sales"})
    .sort_values("sport_sales",ascending=False)
)
