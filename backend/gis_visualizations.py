import streamlit as st
import pandas as pd
import plotly.express as px
import requests

connection_disasters = requests.get("http://ec2-18-226-200-201.us-east-2.compute.amazonaws.com:5000/get_disaster_data").json()
disaster_df = pd.DataFrame(connection_disasters)
disaster_df = disaster_df.drop(['_id', 'description'], axis=1)
disaster_df['month_year'] = pd.to_datetime(disaster_df['declared_date']).dt.strftime('%Y-%m')
disaster_df['lat'] = pd.to_numeric(disaster_df['lat'])
disaster_df['long'] = pd.to_numeric(disaster_df['long'])
disaster_df['radius_miles'] = pd.to_numeric(disaster_df['radius_miles'])

st.title("Disasters in the US")

select_time = st.selectbox("Select Month and Year", ["All"] + sorted(disaster_df['month_year'].unique()))

if select_time == "All":
    filter_df = disaster_df
else:
    filter_df = disaster_df[disaster_df['month_year'] == select_time]

fig_disaster = px.scatter_geo(filter_df, lat = 'lat', lon = 'long', size = 'radius_miles', projection = 'albers usa',
                              hover_name='name', hover_data=['radius_miles'])
fig_disaster.update_geos(
    projection_type="albers usa",
    bgcolor= f"rgb(255, 255, 255)",
    showland=True,
    showcoastlines=True,
    landcolor = 'white',
    coastlinecolor="white", 
)
fig_disaster.update_layout(
    font=dict(color="white"),
    paper_bgcolor=f"rgb(255, 255, 255)",
)
st.plotly_chart(fig_disaster)
