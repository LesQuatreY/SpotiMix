import random
import config
import streamlit as st
import spotify_id_access

from sklearn.cluster import KMeans
from spotify_playlist_fetcher import SpotifyPlaylistFetcher

# """
# Configuration de la page
# """
st.set_page_config(layout="wide")
# Configuration avec des styles CSS pour les différents background
st.markdown('<style>{}</style>'.format(config.main_page_background), unsafe_allow_html=True)


# """
# Demande à l'utilisateur le lien de la playlist
# """
col1, col2 = st.columns(2)
playlist_url = col1.text_input("Insérer le lien de votre playlist Spotify :")
# https://open.spotify.com/playlist/1g5V0tiecUw0zuaKlIsF24?si=9bc6da25690a4ff1

# """
# Demande à l'utilisateur le seuil de la longueur de la nouvelle playlist
# """
playlist_length_threshold = col2.number_input(
    "Entrez la longueur de la nouvelle playlist :", 
    value=0
    )

if not playlist_url: st.stop()
if playlist_length_threshold==0: st.stop()

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
st.info("... Création de la playlist ...")
nb_clusters = int(len(data_for_clustering)/2)
kmeans = KMeans(n_clusters=nb_clusters, max_iter=1000).fit(data_for_clustering)

playlist_genre = tracker.get_playlist_genres(playlist_url)
values = list(playlist_genre.values())
keys = list(playlist_genre.keys())

newPlaylist = []

while len(newPlaylist) < playlist_length_threshold:
    genre = random.choices(
        keys, weights=[value / sum(values) for value in values]
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


col1, col2, col3 = st.columns(3)
col1.write("Musique :")
col2.write("Artistes :")
col3.write("Url de la musique :")
for music in newPlaylist[:playlist_length_threshold]:
    col1.write(tracker.get_track_name(music))
    col2.write(tracker.get_artist_name(music))
    col3.write("https://open.spotify.com/track/" + music)
st.success("Playlist générée !")
