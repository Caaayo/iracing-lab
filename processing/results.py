# Concept:
# Loop over every .json file in data/cache/
# For each file, pull out the top-level session info (track, series, date, etc.)
# Find the Race session inside session_results
# Find your entry inside results using your cust_id
# Combine the top-level info and your result into a signle flat dictionary
# Append that dict to a list
# Return the list as a Pandas DataFrame

import os
import json
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

# My iracing customer ID
CUST_ID = int(os.getenv('CUST_ID'))

def load_results():
    races = []

    for filename in os.listdir('data/cache'):
        if not filename.endswith('.json'):
            continue

        with open(f'data/cache/{filename}') as f:
            raw = json.load(f)

        d = raw['data']

        # Find the Race session
        race_session = None
        for session in d['session_results']:
            if session['simsession_type_name'] == 'Race':
                race_session = session

        if race_session is None:
            continue

        # Find your result
        my_result = None
        for result in race_session['results']:
            if result['cust_id'] == CUST_ID:
                my_result = result

        if my_result is None:
            continue

        # Build the race dict — this must be INSIDE the for filename loop
        race = {
            'track':                    d['track']['track_name'],
            'series':                   d['series_name'],
            'session_type':             session['simsession_type_name'],
            #'start_time':               d['start_time'],
            'start_time': pd.to_datetime(d['start_time']).tz_convert('America/Chicago').strftime('%Y-%m-%d %I:%M %p'), # Convert to Central timezone
            'finish_position':          my_result['finish_position'] + 1,
            'finish_position_in_class': my_result['finish_position_in_class'] + 1,
            #'starting_position':        my_result['starting_position'] + 1,
            'starting_position_in_class': my_result['starting_position_in_class'] + 1,
            'incidents':                my_result['incidents'],
            'laps_complete':            my_result['laps_complete'],
            'oldi_rating':              my_result['oldi_rating'],
            'newi_rating':              my_result['newi_rating'],
            'best_lap_time':            my_result['best_lap_time'] / 10000,
            'best_lap_num':             my_result['best_lap_num'],
            'average_lap':              my_result['average_lap'] / 10000,
            'car_class_name':           my_result['car_class_name'],
            'car_name':                 my_result['car_name'],
        }

        races.append(race)

    return pd.DataFrame(races)

def load_practices():
    practices = []

    for filename in os.listdir('data/cache'):
        if not filename.endswith('.json'):
            continue

        with open(f'data/cache/{filename}') as f:
            raw = json.load(f)

        d = raw['data']

        # Skip files that also have a Race session
        has_race = any(s['simsession_type_name'] == 'Race' for s in d['session_results'])
        if has_race:
            continue

        # Find the practice session
        practice_session = None
        for session in d['session_results']:
            if session['simsession_type_name'] == 'Open Practice':
                practice_session = session

        if practice_session is None:
            continue

        # Find your result
        my_result = None
        for result in practice_session['results']:
            if result['laps_complete'] == 0:
                continue
            if result['cust_id'] == CUST_ID:
                my_result = result

        if my_result is None:
            continue

        # Build the practice dict — this must be INSIDE the for filename loop
        practice = {
            'track':                    d['track']['track_name'],
            'series':                   d['series_name'],
            'session_type':             session['simsession_type_name'],
            'start_time':               d['start_time'],
            'incidents':                my_result['incidents'],
            'laps_complete':            my_result['laps_complete'],
            'best_lap_time':            my_result['best_lap_time'] / 10000,
            'best_lap_num':             my_result['best_lap_num'],
            'average_lap':              my_result['average_lap'] / 10000,
            'car_class_name':           my_result['car_class_name'],
            'car_name':                 my_result['car_name'],
        }

        practices.append(practice)

    return pd.DataFrame(practices)

# Test it when running this file directly
if __name__ == '__main__':
    df_races = load_results()
    df_practices = load_practices()
    print(df_races)
    print(df_races.dtypes)
    print(df_practices)
    print(df_practices.dtypes)
