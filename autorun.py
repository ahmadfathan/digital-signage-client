from kodijson import Kodi, PLAYER_VIDEO
from os import path, listdir 
from time import sleep

'''
Playlist 
0 - Audio
1 - Movie
2 - Picture
'''

def run(type):
    playlist_id = 2 if type in [1,2] else 1

    HOST = 'localhost'
    kodi = Kodi(f'http://{HOST}/jsonrpc', 'osmc', 'osmc')

    movies_path = '/home/osmc/Movies/'
    pictures_path = '/home/osmc/Pictures/'

    files_path = pictures_path if type in [1,2] else movies_path

    kodi.Player.Stop([PLAYER_VIDEO])

    sleep(3)

    result = kodi.Playlist.Clear(playlistid=playlist_id)

    files = listdir(files_path)

    print(playlist_id)

    for file in files:
        kodi.Playlist.Add(playlistid=playlist_id, item={"file": path.join(files_path, file)})

    result = kodi.Player.Open(item={"playlistid" : playlist_id}, options = {"repeat": "all"})

    return result
