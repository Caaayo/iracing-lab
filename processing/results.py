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

# My iracing customer ID
CUST_ID = 924869

def load_results():
    # List to hold one dictionary per race
    races = []

    # Loop over every file in data/cache/
    for filename in os.listdir('data/cache'):
        if not filename.endswith('.json'):
            continue

        # Open and parse the JSON file
        with open(f'data/cache/{filename}') as f:
            raw = json.load(f)

        # Main data lives under the 'data' key
        d = raw['data']

        # Find the Race session from session_results
        race_session = None
        for session in d['session_results']:
            pass

        if race_session is None:
            continue

        # Find your result from race_session['results']
        my_result = None
        for result in race_session['results']:
            # TODO: Check if cust_id matches and assign to my_result
            if result['cust_id'] == CUST_ID:
                my_result = result

        if my_result is None:
            continue

    # Build a flat dictionary combining session info and your result
    # Hint: Lap times are in miliseconds - need to be divided by 10000 to get seconds
    # Hint: finish_position is zero-indexed so add 1
    race = {
        'track':,                       # TODO
        'series':,                      # TODO
        'start_time':,                  # TODO
        'finish_position':,             # TODO
        'finish_position_in_class':,    # TODO
        'starting_position':,           # TODO
        'incidents':,                   # TODO
        'laps_complete':,               # TODO
        'oldi_rating':,                 # TODO
        'newi_rating':,                 # TODO
        'best_lap_time':,               # TODO
        'average_lap':,                 # TODO
        'car_name':,                    # TODO
    }

    races.append(race)

    # Return as a DataFrame
    return pd.DataFrame(races)

# Test it when running this file directly
if __name__ == '__main__':
    df = load_results()
    print(df)
    print(df.dtypes)
