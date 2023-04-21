import random
import string
import spotipy
import spotify_id_access

from sklearn.cluster import KMeans
from spotipy.oauth2 import SpotifyClientCredentials


class SpotifyPlaylistFetcher:
    def __init__(self, client_id, client_secret):
            client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
            self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
    def get_playlist_tracks(self, playlist_link):
        return [self.sp.audio_features(track["track"]["uri"])[0] for track in self.sp.playlist_tracks(playlist_link.split("/")[-1].split("?")[0])["items"]] 
    
    def get_music_tracks(self, music_link):
         return self.sp.audio_features(music_link.split("/")[-1])[0]
    
    def searchNew(self, genre):
          random_char = random.choice(string.ascii_letters)
          query = f'track:"{random_char}" genre:"{genre}"'
          results = self.sp.search(q=query, type="track", limit=50)

          ids_song_to_add = [track["id"] for track in results["tracks"]["items"]]
          audio_features = self.sp.audio_features(tracks=ids_song_to_add)
          return audio_features 

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
