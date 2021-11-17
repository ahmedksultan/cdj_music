import json
import csv
import spotipy
import pandas as pd
import matplotlib.pyplot as plt

from spotipy.oauth2 import SpotifyClientCredentials

client_id = ''
client_secret = ''

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id, client_secret))

data = []

with open('data_short.csv', newline='') as f:
    data_reader = csv.reader(f, delimiter=',')

    # list of tuples -> spotify data -> json
    # basic tuple: (school, major, year, gender, intl/dom, spotify_user, spotify_playlist)

    for row in data_reader:
        if (row[8] == "Yes"):
            # school formatting
            school = row[2]
            school = school[school.find('(') + 1:school.find(')')]
            
            major = row[3]
            year = row[4]
            gender = row[5]
            intl_dom = row[6]

            # url formatting
            sp_prof = row[9]
            sp_play = row[10]

            if (sp_prof.find("?si=") != -1):
                sp_prof = sp_prof[:sp_prof.find("?si=")]

            if (sp_prof.find("user/") != -1):
                sp_prof = sp_prof[sp_prof.find("user/") + 5:]
            
            if (sp_play.find("?si=") != -1):
                sp_play = sp_play[:sp_play.find("?si=")]
            
            data.append((school, major, year, gender, intl_dom, sp_prof, sp_play))

playlist_dict = {}

'''
for user in data:
    user_id = user[5]

    playlists = sp.user_playlists(user_id)
    playlist_dict[user_id] = []

    playlists = playlists["items"]

    for p in playlists:
        playlist_dict[user_id].append(p["uri"])

with open("user_playlists.json", "w") as f:
    json.dump(playlist_dict, f)
'''

with open("user_playlists.json", "r") as f:
    playlist_dict = json.load(f)

# objective: go through all playlists, aggregate all the songs in a json object along with demographic data

aggrsong_dict = {}

for ud, up in zip(data, playlist_dict.keys()):
    user_id = ud[5]

    aggrsong_dict[user_id] = {}
    aggrsong_dict[user_id]["playlists"] = playlist_dict[up]

    aggrsong_dict[user_id]["songs"] = []

    for pl in playlist_dict[up]:
        songs = sp.playlist_tracks(pl)["items"]
        aggrsong_dict[user_id]["songs"].append(songs)

with open("user_songs,json", "w") as f:
    json.dump(aggrsong_dict, f)

