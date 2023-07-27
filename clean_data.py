import numpy as np
import pandas as pd
from tqdm import tqdm

data = pd.read_csv('./match_data.csv', index_col='count')
match_data = data.dropna()
user_data = pd.read_csv('./user_data.csv')
users = user_data['user']
matches_found = {}
for user in tqdm(users):
    user_wins = match_data.loc[match_data['user0'] == user]
    if len(user_wins) == 0:
        continue
    opponents = user_wins['user1']
    user_loses = match_data.loc[match_data['user1'] == user]
    if len(user_loses) == 0:
        continue
    
    for opponent in opponents:
        if (user in matches_found.keys() and opponent in matches_found[user]):
            break
        matches_found[opponent] = []
        matches_found[opponent].append(user)
        
        opp_win = user_loses.loc[user_loses['user0'] == opponent]
        user_win = user_wins.loc[user_wins['user1'] == opponent]
        if (len(opp_win) > len(user_win)):
            match_data.drop(labels=user_win.index, axis=0, inplace=True, errors='ignore')
        elif (len(opp_win) < len(user_win)):
            match_data.drop(labels=opp_win.index, axis=0, inplace=True, errors='ignore')
        else:
            match_data.drop(labels=opp_win.index, axis=0, inplace=True, errors='ignore')
            match_data.drop(labels=user_win.index, axis=0, inplace=True, errors='ignore')
match_data = match_data.drop_duplicates(['user0', 'user1'])

exclude = ['id', 'id0', 'id1', 'user0', 'user1', 'winner']
match_data = match_data.drop(exclude, axis=1)

match_data.to_csv('./cleaned.csv')