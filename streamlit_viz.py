import streamlit as st
import pandas as pd
import plotly.express as px

# to run: streamlit run streamlit_viz.py

df = pd.read_json('data/sfcc_2023_disasters.json')
df = df.drop(['description'], axis=1)
df['month_year'] = pd.to_datetime(df['declared_date']).dt.strftime('%Y-%m')

st.title("Disasters in the US By Year")

select_time = st.selectbox("Select Month and Year", ["All"] + sorted(df['month_year'].unique()))

if select_time == "All":
    filter_df = df
else:
    filter_df = df[df['month_year'] == select_time]

fig = px.scatter_geo(filter_df, lat = 'lat', lon = 'long', size = 'radius_miles', projection = 'albers usa',
                     hover_name='name', hover_data=['radius_miles'])
fig.update_geos(
    projection_type="albers usa",
    bgcolor= f"rgb(14, 17, 23)",
    showland=True,
    landcolor="black",
    showcoastlines=True,
    coastlinecolor="white", 
)
fig.update_layout(
    font=dict(color="white"),  # Text color
    paper_bgcolor=f"rgb(14, 17, 23)",  # Plot area background color
)
st.plotly_chart(fig)
