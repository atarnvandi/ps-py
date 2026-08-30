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

## 4. Most Selling Game by Region
game_sales_by_region = df.groupby(['title'])[['na_sales','jp_sales','pal_sales','other_sales','total_sales']].sum().sort_values('total_sales',ascending=False)
top5_na_reg = (game_sales_by_region
                .sort_values('na_sales', ascending=False)
                .head(5)
                .drop(columns=['jp_sales','pal_sales','other_sales','total_sales'])
                .rename(columns={'na_sales':'sales'})
                )

top5_jp_reg = (game_sales_by_region
                .sort_values('jp_sales', ascending=False)
                .head(5)
                .drop(columns=['na_sales','pal_sales','other_sales','total_sales'])
                .rename(columns={'jp_sales':'sales'})
                )

top5_pal_reg = (game_sales_by_region
                .sort_values('pal_sales', ascending=False)
                .head(5)
                .drop(columns=['na_sales','jp_sales','other_sales','total_sales'])
                .rename(columns={'pal_sales':'sales'})
                )

top5_other_reg = (game_sales_by_region
                .sort_values('other_sales', ascending=False)
                .head(5)
                .drop(columns=['na_sales','jp_sales','pal_sales','total_sales'])
                .rename(columns={'other_sales':'sales'})
                )
#%%
top1_per_reg = pd.concat([top5_na_reg.head(1),top5_jp_reg.head(1),top5_pal_reg.head(1),top5_other_reg.head(1)])
top1_per_reg['Region'] = ['North America','Japan','Europe and Africa','Rest of World']
# %%

# Visualization - MULTI
fig, ax = plt.subplots(2,2, figsize=(10,5))
ax[0,0].barh(top5_game['title'], top5_game['total_sales'], height=0.4)
ax[0,0].invert_yaxis()
ax[0,0].tick_params(axis='x', rotation=90)

ax[0,1].barh(top5_genre['genre'], top5_genre['total_sales'], height=0.4)
ax[0,1].invert_yaxis()
ax[0,1].tick_params(axis='x', rotation=90)

ax[1,0].barh(top5_console['console'], top5_console['total_sales'], height=0.4)
ax[1,0].invert_yaxis()
ax[1,0].tick_params(axis='x', rotation=90)

# %%

# Visualization - Single
## 1. Top 5 Game by Sales
fig1, ax1 = plt.subplots(figsize=(10,5))
ax1.barh(top5_game['title'], top5_game['total_sales'], height=0.4)
ax1.invert_yaxis()
ax1.tick_params(axis='x', rotation=90)

## 2. Top 5 Genre by Sales
fig2, ax2 = plt.subplots(figsize=(10,5))
ax2.barh(top5_genre['genre'], top5_genre['total_sales'], height=0.4)
ax2.invert_yaxis()
ax2.tick_params(axis='x', rotation=90)

## 3. Top 5 Console by Game Sales
fig3, ax3 = plt.subplots(figsize=(10,5))
ax3.barh(top5_console['console'], top5_console['total_sales'], height=0.4)
ax3.invert_yaxis()
ax3.tick_params(axis='x', rotation=90)

# %%

data = {
        'insight':['Most selling game by title',
                'Most selling game by genre',
                'Most selling game by console',
                'Most selling game in North America',
                'Most selling game in Japan',
                'Most selling game in Europe and Africa',
                'Most selling game in Rest of The World'],

        'finding':[top5_game.iloc[0,0],
                top5_genre.iloc[0,0],
                top5_console.iloc[0,0],
                top5_na_reg.index[0],
                top5_jp_reg.index[0],
                top5_pal_reg.index[0],
                top5_other_reg.index[0]],

        'supporting_data':['top5_game',
                        'top5_genre',
                        'top5_console',
                        'top5_na_reg',
                        'top5_jp_reg',
                        'top5_pal_reg',
                        'top5_other_reg'],
        
        'recomendation':['','','','','','','']
}
insight_df = pd.DataFrame(data)

# insight_df.to_csv('insight.csv',index=False)