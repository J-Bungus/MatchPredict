import requests as req
import pandas as pd
from tqdm import tqdm
import csv


user_data = pd.read_csv('./user_data.csv')
user_data.set_index('count', inplace=True)
print(user_data)
user_ids = user_data['id']

API_BASE = 'https://ch.tetr.io/api/streams/league_userrecent_'

match_data = []
match_id = {}
with open ('./match_data_alt.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=[
        "id",
        "id0",
        "user0",
        "wr0",
        "rating0",
        "apm0",
        "pps0",
        "vs0",
        "id1",
        "user1",
        "wr1",
        "rating1",
        "apm1",
        "pps1",
        "vs1",
        "winner"
    ])

    writer.writeheader()
    for id in tqdm(user_ids):
        try:
            r = req.get(API_BASE + id)
        except ConnectionError as e:
            print(e)
            print(f"No Data from: {id}")
            continue
        
        r = r.json()
        match_history = r['data']['records']

        for match in match_history:
            if match['_id'] in match_id:
                continue
            match_id[match['_id']] = match['_id']
            endcontext = match['endcontext']
            id0 = endcontext[0]['user']['_id']
            id1 = endcontext[1]['user']['_id']
            p0_data = user_data.loc[user_data['id'] == id0]
            p1_data = user_data.loc[user_data['id'] == id1]

            if (p0_data.empty or p1_data.empty):
                continue

            p0 = {
                "id0": id0,
                "user0": p0_data.iloc[0,1],
                "wr0": p0_data.iloc[0,3] / p0_data.iloc[0,2],
                "rating0": p0_data.iloc[0,4],
                "apm0": p0_data.iloc[0,6],
                "pps0": p0_data.iloc[0,7],
                "vs0": p0_data.iloc[0,8]
            }
            p1 = {
                "id1": id1,
                "user1": p1_data.iloc[0,1],
                "wr1": p1_data.iloc[0,3]/ p1_data.iloc[0,2],
                "rating1": p1_data.iloc[0,4],
                "apm1": p1_data.iloc[0,6],
                "pps1": p1_data.iloc[0,7],
                "vs1": p1_data.iloc[0,8]
            }

            match = {
                "id": match['_id'],
                **p0,
                **p1,
                "winner": 0, 
            }

            writer.writerow(match)
            match_data.append(match)


match_df = pd.DataFrame(match_data)
match_df.to_csv('./match_data.csv')