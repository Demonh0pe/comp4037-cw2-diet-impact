import pandas as pd
import numpy as np
import plotly.express as px

df = pd.read_csv('Results_21Mar2022.csv')
df_run1 = df[df['mc_run_id'] == 1]

metrics = ['mean_ghgs', 'mean_land', 'mean_watscar',
           'mean_eut', 'mean_bio', 'mean_acid']

diet_types = df_run1['diet_group'].unique()
result = []

for diet in diet_types:
    sub = df_run1[df_run1['diet_group'] == diet]
    total_n = sub['n_participants'].sum()
    row = [diet]
    for m in metrics:
        weighted_mean = (sub[m] * sub['n_participants']).sum() / total_n
        row.append(weighted_mean)
    result.append(row)

df_diet = pd.DataFrame(result, columns=[
    'Diet', 'GHG Emissions', 'Land Use', 'Water Scarcity',
    'Eutrophication', 'Biodiversity', 'Acidification'
])


for col in df_diet.columns[1:]:
    df_diet[col] = df_diet[col] / df_diet[col].max()

df_diet = df_diet.set_index('Diet').loc[['meat100', 'meat', 'meat50', 'fish', 'vegan']].reset_index()
df_diet['Diet'] = df_diet['Diet'].map({
    'meat100': 'High Meat',
    'meat': 'Medium Meat',
    'meat50': 'Low Meat',
    'fish': 'Fish-based',
    'vegan': 'Vegan'
})


fig = px.parallel_coordinates(
    df_diet,
    color="GHG Emissions",
    dimensions=[
        'GHG Emissions', 'Land Use', 'Water Scarcity',
        'Eutrophication', 'Biodiversity', 'Acidification'
    ],
    color_continuous_scale=px.colors.sequential.Reds_r,
    labels={
        "GHG Emissions": "GHG Emissions",
        "Land Use": "Land Use",
        "Water Scarcity": "Water Scarcity",
        "Eutrophication": "Eutrophication",
        "Biodiversity": "Biodiversity",
        "Acidification": "Acidification"
    }
)

fig.update_layout(
    title="Environmental Impact Across Different Diet Types (Normalized)",
    title_x=0.5,
    title_y=0.98,
    font=dict(size=14),
    margin=dict(l=50, r=50, t=120, b=50)
)

fig.show()
