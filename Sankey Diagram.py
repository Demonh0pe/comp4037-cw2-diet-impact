import pandas as pd
import plotly.graph_objects as go


df = pd.read_csv("Results_21Mar2022.csv")
df = df[df['mc_run_id'] == 1]


df['ghg_total'] = df['mean_ghgs'] * df['n_participants']


df['sex'] = df['sex'].str.lower()
df['diet'] = df['diet_group']
df['age'] = df['age_group']


df_sankey = df[['sex', 'diet', 'age', 'ghg_total']]


all_sex = df_sankey['sex'].unique().tolist()
all_diet = df_sankey['diet'].unique().tolist()
all_age = df_sankey['age'].unique().tolist()

labels = all_sex + all_diet + all_age


label_map = {label: i for i, label in enumerate(labels)}


link_1 = df_sankey.groupby(['sex', 'diet'])['ghg_total'].sum().reset_index()
source_1 = link_1['sex'].map(label_map)
target_1 = link_1['diet'].map(label_map)
value_1 = link_1['ghg_total']

link_2 = df_sankey.groupby(['diet', 'age'])['ghg_total'].sum().reset_index()
source_2 = link_2['diet'].map(label_map)
target_2 = link_2['age'].map(label_map)
value_2 = link_2['ghg_total']


source = pd.concat([source_1, source_2]).tolist()
target = pd.concat([target_1, target_2]).tolist()
value = pd.concat([value_1, value_2]).tolist()


fig = go.Figure(data=[go.Sankey(
    arrangement='snap',
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=labels,
        color="lightblue"
    ),
    link=dict(
        source=source,
        target=target,
        value=value,
        color="rgba(255,100,100,0.4)"
    )
)])

fig.update_layout(
    title_text="Sankey Diagram: Sex → Diet → Age (GHG Weighted Flow)",
    title_x=0.5,
    font=dict(size=12)
)

fig.show()
