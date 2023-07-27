import requests as req
import pandas as pd
from dataclasses import dataclass

api = 'https://ch.tetr.io/api/users/lists/league/all'

@dataclass
class UserData:
    """class for storing user data"""
    id: str
    user: str
    gamesplayed: int
    gameswon: int
    rating: float
    glicko: float
    apm: float
    pps: float
    vs: float

# Make API call for all ranked users
r = req.get(api).json()
users = r['data']['users'] # extract the list of user objects

# extract data and create an instance of the class
data = map(
    lambda x: UserData(
        x['_id'], 
        x['username'], 
        x['league']['gamesplayed'],
        x['league']['gameswon'],
        x['league']['rating'],
        x['league']['glicko'],
        x['league']['apm'],
        x['league']['pps'],
        x['league']['vs']),
    users
)

user_df = pd.DataFrame(data)

user_df.to_csv('./user_data.csv')