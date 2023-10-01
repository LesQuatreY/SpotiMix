import random
import string
import spotipy

from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials

class SpotifyPlaylistFetcher:
    def __init__(self, client_id, client_secret):
            client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
            auth_manager = SpotifyOAuth(
                 client_id=client_id, client_secret=client_secret,
                redirect_uri="https://example.com/callback", 
                scope="playlist-modify-public playlist-modify-private",
                username="tqnguy"
                )
            self.sp_create = spotipy.Spotify(auth_manager=auth_manager)
            self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
    def get_playlist_tracks(self, playlist_link):
        return [self.sp.audio_features(track["track"]["uri"])[0] for track in self.sp.playlist_tracks(playlist_link.split("/")[-1].split("?")[0])["items"]]
        
    def get_music_tracks(self, music_link):
         return self.sp.audio_features(music_link.split("/")[-1])[0]
    
    def get_playlist_genres(self, playlist_link):
         return {genre:sum(1 for track in self.sp.playlist_tracks(playlist_link)['items'] for artist in track['track']['artists'] if genre in self.sp.artist(artist['id'])['genres']) for genre in set(genre for track in self.sp.playlist_tracks(playlist_link)['items'] for artist in track['track']['artists'] for genre in self.sp.artist(artist['id'])['genres'])}

    def searchNew(self, genre):
          random_char = random.choice(string.ascii_letters)
          query = f'track:"{random_char}" genre:"{genre}"'
          results = self.sp.search(q=query, type="track", limit=50)
          ids_song_to_add = [track["id"] for track in results["tracks"]["items"]]
          audio_features = self.sp.audio_features(tracks=ids_song_to_add)
          return audio_features 
    
    def create_playlist(self, playlist_name, track_ids, description=None, public=True):
        playlist = self.sp_create.user_playlist_create(user=self.sp_create.me()['id'],
                                                name=playlist_name,
                                                public=public,
                                                description=description)
        self.sp_create.playlist_add_items(playlist["id"], track_ids)

    def get_track_name(self, track_id):
         return self.sp.track(track_id)['name']    
    
    def get_artist_name(self, track_id):
         return ', '.join([artist['name'] for artist in self.sp.track(track_id)['artists']])