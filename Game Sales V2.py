# %% Importing Libraries
import matplotlib.pyplot as plt
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

## One Title Has Different Genres Across Consoles

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
## Sports Game Title Sales - What Game Titles Drives The Sports Game Genre
sports_titles_by_sales = (
    df[df["genre"] == "Sports"]
    .groupby("title")["total_sales"]
    .sum()
    .nlargest(20)
    .reset_index()
    .rename(columns={"total_sales": "sport_sales"})
    .sort_values("sport_sales", ascending=False)
)

top_5_sports_titles_by_sales = sports_titles_by_sales.nlargest(5, columns="sport_sales")

## Action-Adventure Game Title Sales - Double Check on GTA V
action_titles_by_sales = (
    df[(df["genre"] == "Action") | (df["genre"] == "Action-Adventure")]
    .groupby("title")["total_sales"]
    .sum()
    .nlargest(20)
    .reset_index()
    .rename(columns={"total_sales": "action_sales"})
    .sort_values("action_sales", ascending=False)
)
top_5_action_titles_by_sales = action_titles_by_sales.nlargest(
    5, columns="action_sales"
)

## 1st Rank Sports Game Title Vs 1st Rank Action/ Action-Adventure Genre
top_1_sports_game = sports_titles_by_sales.iloc[0, 0]
top_1_action_game = action_titles_by_sales.iloc[0, 0]

top_1_action_game_console_by_sales = (
    df[(df["title"] == top_1_action_game)]
    .groupby(["title", "console"])["total_sales"]
    .sum()
    .nlargest(5)
    .reset_index()
    .rename(columns={"total_sales": "action_sales"})
    .sort_values("action_sales", ascending=False)
)

top_1_sports_game_console_by_sales = (
    df[(df["title"] == top_1_sports_game)]
    .groupby(["title", "console"])["total_sales"]
    .sum()
    .nlargest(5)
    .reset_index()
    .rename(columns={"total_sales": "sports_sales"})
    .sort_values("sports_sales", ascending=False)
)

# %% Visualization
fig, ax = plt.subplots(1, 2)

ax[0].barh(
    width=top_1_sports_game_console_by_sales["sports_sales"],
    y=top_1_sports_game_console_by_sales["console"],
    label=top_1_sports_game_console_by_sales["sports_sales"],
)
ax[1].barh(
    width=top_1_action_game_console_by_sales["action_sales"],
    y=top_1_action_game_console_by_sales["console"],
    label=top_1_action_game_console_by_sales["action_sales"],
)

ax[0].set_title("FIFA 15 Sales on Consoles")
ax[1].set_title("GTA V Sales on Consoles")

ax[0].set_xlabel("Sales in Million")
ax[1].set_xlabel("Sales in Million")

plt.show()

## Sports Game Vs Actions Game Sales Distribution
fig1, ax1 = plt.subplots(1, 2, figsize=(10, 8))

ax1[0].bar(
    height=sports_titles_by_sales["sport_sales"],
    x=sports_titles_by_sales["title"],
    label=sports_titles_by_sales["sport_sales"],
)
ax1[1].bar(
    height=action_titles_by_sales["action_sales"],
    x=action_titles_by_sales["title"],
    label=action_titles_by_sales["action_sales"],
)

ax1[0].tick_params(axis="x", rotation=90)
ax1[1].tick_params(axis="x", rotation=90)
