import streamlit as st
import plotly.express as px
import sys
import os

from processing.results import load_results, load_practices
#from dotenv import load_dotenv
#load_dotenv()

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.title("Analysis")

df_races = load_results()
df_practices = load_practices()

# -- Car Filter
cars = df_races['car_name'].unique().tolist()
selected_car = st.selectbox("Select Car", cars)

# -- Filter data to selected car
df_races_car = df_races[df_races['car_name'] == selected_car].sort_values('start_time')
df_practices_car = df_practices[df_practices['car_name'] == selected_car].sort_values('start_time')

# -- Plot (Average vs Best Lap Time)
fig = px.line(
        df_races_car,
        x='start_time',
        y=['best_lap_time', 'average_lap'],
        title="Average vs Best Lap Time", 
        labels={
          "start_time": "Date",
          "best_lap_time": "Best Lap Time",
          "average_lap": "Avg Lap Time",
        },
        markers=True
)

st.plotly_chart(fig)

# -- Plot (Consistency Gap)
df_races_car['consistency_gap'] = df_races_car['average_lap'] - df_races_car['best_lap_time']

fig2 = px.line(
        df_races_car,
        x='start_time',
        y='consistency_gap',
        title="Consistency Gap (Avg - Best Lap)", 
        labels={
          "start_time": "Date",
          "consistency_gap": "Consistency Gap (s)",
        },
        markers=True
)

st.plotly_chart(fig2)


# -- Plot (Position Change)
df_races_car['positions_gained'] = df_races_car['starting_position'] - df_races_car['finish_position']

df_races_car['position_change'] = df_races_car['positions_gained'].apply(
        lambda x: f'+{x}' if x > 0 else str(x))

df_races_car['result'] = df_races_car['positions_gained'].apply(
        lambda x: 'Gained' if x > 0 else 'None' if x == 0 else 'Lost')

fig3 = px.bar(
    df_races_car,
    x='start_time',
    y='positions_gained',
    title="Positions Gained/Lost per Race",
    labels={
        "start_time": "Date",
        "positions_gained": "Positions",
    },
    color='result',
    color_discrete_map={
        'Gained': 'green',
        'None': 'gray',
        'Lost': 'red'
    },
    custom_data=[
        'series', 
        'track', 
        'start_time', 
        'car_name', 
        'starting_position', 
        'finish_position', 
        'position_change',
    ]
)

fig3.update_traces(
    hovertemplate=(
        "<b>%{customdata[3]}</b><br>"       # Car
        "Series: %{customdata[0]}<br>"      # Series
        "Track: %{customdata[1]}<br>"       # Track
        "Date: %{customdata[2]}<br>"        # Date
        "Started: P%{customdata[4]}<br>"    # Starting Position
        "Finished: P%{customdata[5]}<br>"   # Finish Position
        "Change: %{customdata[6]}<br>"      # Position Change
        "<extra></extra>"
    )
)
st.plotly_chart(fig3)
