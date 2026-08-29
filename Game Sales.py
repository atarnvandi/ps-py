# %%
import matplotlib.pyplot as plt
import pandas as pd

# %% 
data_dict = pd.read_csv('vg_data_dictionary.csv')
raw_data = pd.read_csv('vgchartz-2024.csv')

# %%
df = raw_data.copy()
# Data Cleaning
df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
to_fill = {'critic_score': 0,'total_sales': 0,'na_sales': 0,'jp_sales': 0,'pal_sales': 0,'other_sales': 0}
df = df.fillna(to_fill)
df['total_sales'] = df[['na_sales', 'pal_sales', 'jp_sales', 'other_sales']].sum(axis=1)
df = df.drop(columns=['img','last_update'])
df['developer'] = df['developer'].fillna(df['publisher'])

# %%

# Exploratory Data Analysis
## 1. Most Selling Game by Title

top5_game = df.groupby(['title'])['total_sales'].sum().to_frame('total_sales').reset_index().sort_values('total_sales', ascending=False).head(5)

## 2. Most Selling Game by Genre
top5_genre = df.groupby(['genre'])['total_sales'].sum().to_frame('total_sales').reset_index().sort_values('total_sales', ascending=False).head(5)

## 3. Most Selling Game by Console
top5_console = df.groupby(['console'])['total_sales'].sum().to_frame('total_sales').reset_index().sort_values('total_sales', ascending=False).head(5)

# %%

# Visualization
fig1, ax = plt.subplots(2,2, figsize=(10,5),sharex='col')
ax[0,0].barh(top5_game['title'], top5_game['total_sales'], height=0.4)
ax[0,0].invert_yaxis()
# ax[0,0].tick_params(axis='x', rotation=90)

ax[0,1].barh(top5_genre['genre'], top5_genre['total_sales'], height=0.4)
ax[0,1].invert_yaxis()
# ax[0,1].tick_params(axis='x', rotation=90)

ax[1,0].barh(top5_console['console'], top5_console['total_sales'], height=0.4)
ax[1,0].invert_yaxis()
# ax[1,0].tick_params(axis='x', rotation=90)

# %%

data = {
        'insight':['Most selling game by title','Most selling game by genre','Most selling game by console'],
        'finding':[top5_game.iloc[0,0],top5_genre.iloc[0,0],top5_console.iloc[0,0]],
        'supporting_data':['top5_game','top5_genre','top5_console'],
        'recomendation':['','','']
}
insight_df = pd.DataFrame(data)

# insight_df.to_csv('insight.csv',index=False)