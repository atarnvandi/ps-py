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

