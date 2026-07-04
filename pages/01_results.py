import streamlit as st
import plotly.express as px
import sys
import os
from processing.results import load_results, load_practices
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

CUST_ID = int(os.getenv('CUST_ID'))

if st.button("Refresh Data"):
    st.rerun()

st.title("Race Results")

tab_races, tab_practices = st.tabs(["Races", "Practices"])

df_races = load_results()
df_practices = load_practices()

#st.dataframe(df_races)
#st.dataframe(df_practices)

with tab_races:
    st.dataframe(df_races)

with tab_practices:
    st.dataframe(df_practices)

# -- Metric Calculation --
df_races_sorted = df_races.sort_values('start_time')
df_practice_sorted = df_practices.sort_values('start_time')
irating_change = df_races_sorted['newi_rating'].iloc[-1] - df_races_sorted['oldi_rating'].iloc[0]

# -- Plot Creation --
fig = px.line(df_races_sorted, 
              x='start_time', 
              y='newi_rating', 
              title="iRating Over Time", 
              labels={
                  "start_time": "Date",
                  "newi_rating": "iRating",
              },
              markers=True
)

# -- Column Placement --

cols = st.columns(5)
c = {
    'irating':          cols[0],
    'races':            cols[1],
    'practices':        cols[2],
    'avg_finish':       cols[3],
    'avg_inc':          cols[4],
}

with c['irating']:
    st.metric("Current iRating", df_races_sorted['newi_rating'].iloc[-1], delta=irating_change)
with c['races']:
    st.metric("Total Races", len(df_races))
with c['practices']:
    st.metric("Total Practices", len(df_practices))
with c['avg_finish']:
    st.metric("Average Finishing Position", int(df_races['finish_position_in_class'].mean()))
with c['avg_inc']:
    st.metric("Average Incidents", int(df_races['incidents'].mean()))

st.plotly_chart(fig)
