# %% Import Libraries
import matplotlib.pyplot as plt
import pandas as pd

# %% Load Data
raw_df = pd.read_csv("vgchartz-2024.csv")

# %% Data Cleaning
df = raw_df.copy().drop(columns=["img", "last_update"])

df["developer"] = df["developer"].fillna("Unknown")

sales_cols = ["total_sales", "na_sales", "jp_sales", "pal_sales", "other_sales"]
df[sales_cols] = df[sales_cols].fillna(0)

df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")

# Note: one title can have different genres across consoles — not deduplicated,
# since analysis here is at title+console level, not title-only.

# %% Exploratory Data Analysis

# 1. Top 5 Best-Selling Titles
top_game_by_sales = (
    df.groupby("title")["total_sales"]
    .sum()
    .nlargest(5)
    .reset_index()
)

# 2. Top 5 Best-Selling Genres
top_genre_by_sales = (
    df.groupby("genre")["total_sales"]
    .sum()
    .nlargest(5)
    .reset_index()
)

# 3. Top 5 Title-Console Combinations by Sales
top_game_console_by_sales = (
    df.groupby(["title", "console"])["total_sales"]
    .sum()
    .nlargest(5)
    .reset_index()
)

# 4. Top 5 Console-Genre Combinations by Sales
top_console_genre_by_sales = (
    df.groupby(["console", "genre"])["total_sales"]
    .sum()
    .nlargest(5)
    .reset_index()
)
# Top genres overall: Sports, Action, Shooter, Misc, Racing

# %% Question: Why is GTA V the top-selling title if Sports is the top genre?

def top_titles_by_genre(data: pd.DataFrame, genres: list[str], sales_col_name: str, n: int = 20) -> pd.DataFrame:
    """Return top-N titles by summed total_sales for the given genre(s)."""
    return (
        data[data["genre"].isin(genres)]
        .groupby("title")["total_sales"]
        .sum()
        .nlargest(n)
        .reset_index()
        .rename(columns={"total_sales": sales_col_name})
        .sort_values(sales_col_name, ascending=False)
    )


def title_sales_by_console(data: pd.DataFrame, title: str, sales_col_name: str, n: int = 5) -> pd.DataFrame:
    """Return console-level sales breakdown for a single title."""
    return (
        data[data["title"] == title]
        .groupby(["title", "console"])["total_sales"]
        .sum()
        .nlargest(n)
        .reset_index()
        .rename(columns={"total_sales": sales_col_name})
        .sort_values(sales_col_name, ascending=False)
    )


sports_titles_by_sales = top_titles_by_genre(df, ["Sports"], "sport_sales")
action_titles_by_sales = top_titles_by_genre(df, ["Action", "Action-Adventure"], "action_sales")

top_5_sports_titles_by_sales = sports_titles_by_sales.head(5)
top_5_action_titles_by_sales = action_titles_by_sales.head(5)

top_1_sports_game = sports_titles_by_sales.iloc[0, 0]
top_1_action_game = action_titles_by_sales.iloc[0, 0]

top_1_sports_game_console_by_sales = title_sales_by_console(df, top_1_sports_game, "sports_sales")
top_1_action_game_console_by_sales = title_sales_by_console(df, top_1_action_game, "action_sales")

# %% Visualization — Top Title Sales by Console (Sports vs Action)
fig, ax = plt.subplots(1, 2, figsize=(10, 5))

ax[0].barh(
    top_1_sports_game_console_by_sales["console"],
    top_1_sports_game_console_by_sales["sports_sales"],
)
ax[0].set_title(f"{top_1_sports_game} Sales by Console")
ax[0].set_xlabel("Sales (Millions)")

ax[1].barh(
    top_1_action_game_console_by_sales["console"],
    top_1_action_game_console_by_sales["action_sales"],
)
ax[1].set_title(f"{top_1_action_game} Sales by Console")
ax[1].set_xlabel("Sales (Millions)")

fig.tight_layout()
plt.show()

# %% Visualization — Sports vs Action Top-20 Title Distribution
fig1, ax1 = plt.subplots(1, 2, figsize=(10, 8))

ax1[0].bar(sports_titles_by_sales["title"], sports_titles_by_sales["sport_sales"])
ax1[0].set_title("Top 20 Sports Titles by Sales")
ax1[0].tick_params(axis="x", rotation=90)

ax1[1].bar(action_titles_by_sales["title"], action_titles_by_sales["action_sales"])
ax1[1].set_title("Top 20 Action Titles by Sales")
ax1[1].tick_params(axis="x", rotation=90)

fig1.tight_layout()
plt.show()

# Insight: Sports genre sales are spread across many titles (subtler drop-off),
# while GTA V is a clear outlier within the Action genre — a single title
# outperforming the entire genre's typical distribution.