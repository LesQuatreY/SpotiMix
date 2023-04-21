import pandas as pd
import streamlit as st
import spotify_id_access

from sklearn.cluster import KMeans
from spotify_playlist_fetcher import SpotifyPlaylistFetcher

tracker = SpotifyPlaylistFetcher(spotify_id_access.client_id, spotify_id_access.client_secret)

data_for_clustering = [
     [track[key] for key in ['acousticness', 'danceability', 'energy', 'instrumentalness', 'loudness', 'speechiness', 'tempo']]
for track in tracker.get_playlist_tracks("https://open.spotify.com/playlist/1g5V0tiecUw0zuaKlIsF24?si=9bc6da25690a4ff1")
]

nb_clusters = int(len(data_for_clustering)/2)
kmeans = KMeans(n_clusters=nb_clusters, max_iter=1000).fit(data_for_clustering)

to_add = tracker.searchNew("rap")
newPlaylist = []

for elem in to_add:
    to_pred = [[elem["acousticness"], elem["danceability"], elem["energy"],elem["instrumentalness"], elem["loudness"], elem["speechiness"], elem["tempo"]]]
    kmeans.predict(to_pred)
    score = abs(kmeans.score(to_pred))
    if score < 0.90 and elem["id"] not in newPlaylist:
        newPlaylist.append(elem["id"])
        print("score for "+elem["id"]+" : ", score,"| Len new playlist : ", len(newPlaylist))
    
    if len(newPlaylist) >= 35:
        print("quit")
        break