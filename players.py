import vlc
import os

class VLCMediaPlayer:
	def __init__(self, path = '/home/orangepi/Videos'):
		self._path = path

		self._mp = vlc.MediaListPlayer()

		self._mp.get_media_player().set_fullscreen(True)

		self._player = vlc.Instance()

		self._media_list = self._player.media_list_new()

		self.refresh()

	def refresh(self):
		dir_list = os.listdir(self._path)
		for fn in dir_list:
			if fn.endswith('.mp4'):
				self._media_list.add_media(self._player.media_new(os.path.join(self._path, fn)))

	def play(self):
		self._mp.set_media_list(self._media_list)
		self._mp.play()
