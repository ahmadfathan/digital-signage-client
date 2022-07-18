import vlc
import os

PATH = '/home/orangepi/Videos'

dir_list = os.listdir(PATH)

mp = vlc.MediaListPlayer()

mp.get_media_player().set_fullscreen(True)

player = vlc.Instance()

media_list = player.media_list_new()

for fn in dir_list:
	if fn.endswith('.mp4'):
		print(fn)
		media_player = player.media_new(os.path.join(PATH, fn))

		media_list.add_media(media_player)

mp.set_media_list(media_list)

mp.play()

while True: pass
