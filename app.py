import random
import streamlit as st
import spotify_id_access

from sklearn.cluster import KMeans
from spotify_playlist_fetcher import SpotifyPlaylistFetcher

# """
# Demande à l'utilisateur le lien de la playlist
# """
playlist_url = st.text_input("Insérer le lien de votre playlist Spotify :")
# https://open.spotify.com/playlist/1g5V0tiecUw0zuaKlIsF24?si=9bc6da25690a4ff1
if not playlist_url: st.stop()

# """
# Demande à l'utilisateur le seuil de la longueur de la nouvelle playlist
# """
playlist_length_threshold = st.number_input("Entrez la longueur minimale de la nouvelle playlist :", min_value=1, value=10, step=1)

# """
# Récupération des informations des musiques de la playlist
# """
tracker = SpotifyPlaylistFetcher(spotify_id_access.client_id, spotify_id_access.client_secret)
data_for_clustering = [
     [track[key] for key in ['acousticness', 'danceability', 'energy', 'instrumentalness', 'loudness', 'speechiness', 'tempo']]
for track in tracker.get_playlist_tracks(playlist_url)
]

# """
# Classification avec Kmeans
# """
nb_clusters = int(len(data_for_clustering)/2)
kmeans = KMeans(n_clusters=nb_clusters, max_iter=1000).fit(data_for_clustering)

values = list(tracker.get_playlist_genres(playlist_url).values())

newPlaylist = []
while len(newPlaylist) < playlist_length_threshold:
    genre = random.choices(
        list(tracker.get_playlist_genres(playlist_url).keys()), 
        weights=[value / sum(values) for value in values]
        )[0]
    for elem in tracker.searchNew(genre):
        to_pred = [[elem["acousticness"], elem["danceability"], elem["energy"],elem["instrumentalness"], elem["loudness"], elem["speechiness"], elem["tempo"]]]
        kmeans.predict(to_pred)
        score = abs(kmeans.score(to_pred))
        if score < 0.90 and elem["id"] not in newPlaylist:
            newPlaylist.append(elem["id"])
            print("score for "+elem["id"]+" : ", score,"| Len new playlist : ", len(newPlaylist))
        
        if len(newPlaylist) >= 35:
            print("quit")
            break
    st.progress(len(newPlaylist), "En progression...")

for music in newPlaylist:
    st.write("https://open.spotify.com/track/" + music)
