import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from processing.results import load_results

st.title("Race Results")

df = load_results()

st.dataframe(df)

# -- Metric Calculation --
df_sorted = df.sort_values('start_time')
irating_change = df_sorted['newi_rating'].iloc[-1] - df_sorted['oldi_rating'].iloc[0]

cols = st.columns(5)
c = {
    'irating':       cols[0],
    'races':         cols[1],
    'avg_finish':    cols[2],
    'avg_inc':       cols[3],
}

with c['irating']:
    st.metric("Current iRating", df_sorted['newi_rating'].iloc[-1], delta=irating_change)
with c['races']:
    st.metric("Total Races", len(df))
with c['avg_finish']:
    st.metric("Average Finishing Position", int(df['finish_position_in_class'].mean()))
with c['avg_inc']:
    st.metric("Average Incidents", int(df['incidents'].mean()))
