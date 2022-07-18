import requests
import os

class Poller:

	def __init__(self, type, host = 'http://digital-signage.ibncorp.co.id:3000', dev_id = '3de90b9e-f304-43b5-aa17-1544fe780a63'):
		self._host = host
		self._dev_id = dev_id
		self._type = type

	def set_dir(self, picture_dir = '/home/orangepi/Pictures', video_dir = '/home/orangepi/Videos'):
		self._picture_dir = picture_dir
		self._video_dir = video_dir

	def set_media_player(self, run_media_player):
		self._run_media_player = run_media_player

	def download_file(self, save_dir, url, fn, ext):
		print(f'Downloading {fn}..')
		r = requests.get(url, stream = True)
		with open(f"{save_dir}/{fn}.{ext}", "wb") as file:
			for chunk in r.iter_content(chunk_size=1024): 
				if chunk: file.write(chunk)

	def run(self):
		url = f'{self._host}/auth/login'
		body = {
        	'email': 'digital-signage@ibncorp.com',
        	'password': f'12345678'
    	}
		
		x = requests.post(url, json = body)
		resp = x.json()
		
		token = resp['results']['data']['accessToken']
		
		headers = {"authorization": f"Bearer {token}"}
		
		x = requests.get(f'{self._host}/content?deviceId={self._dev_id}', headers = headers)
		
		resp = x.json()

		contents = resp['results']['data']

		dir_list = []

		if self._type == 3:
			dir_list.extend(os.listdir(self._video_dir))
		
		elif type == 1 or type == 2:
			dir_list.extend(os.listdir(self._picture_dir))
		
		print(f'Got {len(contents)} from server!')
		
		added = 0
		removed = 0
		
		content_list = []
		
		for content in contents:
			media = content['media']
			filename = f"{media['fileName']}"
			ext = f"{media['mimeType'].split('/')[1]}"
			media_type = media['type']
			
			media_url = f'{self._host}/media/download/{filename}'
			
			content_list.append(f"{filename}.{ext}")
			
			if not f"{filename}.{ext}" in dir_list:
				if media_type == 1:
					self.download_file(self._picture_dir, media_url, filename, ext)
				elif media_type == 2:
					self.download_file(self._video_dir, media_url, filename, ext)
			
			added = added + 1
			
			DIR = self._picture_dir if type in [0,1] else self._video_dir
			
			for file in dir_list:
				if not file in content_list:
					if os.path.exists(os.path.join(DIR, file)):
						os.remove(os.path.join(DIR, file))
						removed = removed + 1
		
		if added > 0 or removed > 0:
			self._run_media_player()
			print(f'(+) Added {added} file(s)')
			print(f'(-) Removed {removed} file(s)')
		else:
			print('Already Updated!')
