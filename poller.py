import requests
import os
import autorun

class Poller:
	def __init__(self, host = 'http://digital-signage.ibncorp.co.id:3000', dev_id = '3de90b9e-f304-43b5-aa17-1544fe780a63', type):
		self._host = host
		self._dev_id = dev_id
	def set_dir(self, picture_dir = '/home/orangepi/Pictures', video_dir = '/home/orangepi/Videos'):
		self._picture_dir = picture_dir
		self._video_dir = video_dir

	def download_file(self, save_dir, url, fn, ext):
    		print(f'Downloading {fn}..')
    		r = requests.get(url, stream = True)
    		with open(f"{save_dir}/{fn}.{ext}", "wb") as file:
        		for chunk in r.iter_content(chunk_size=1024):
            			if chunk: file.write(chunk)
	def run(self, type):
		x = requests.get(f'{HOST}/content?deviceId={DEVICE_ID}')

    		resp = x.json()

		contents = resp['results']['data']

		dir_list = []

		if type == 3:
        		dir_list.extend(os.listdir(VIDEO_DIR))
		elif type == 1 or type == 2:
			dir_list.extend(os.listdir(PICTURE_DIR))

    		print(f'Got {len(contents)} from server!')

    		added = 0
    		removed = 0

    		content_list = []

    		for content in contents:
        		media = content['media']
        		filename = f"{media['fileName']}"
        		ext = f"{media['mimeType'].split('/')[1]}"
        		media_type = media['type']

        		media_url = f'{HOST}/media/download/{filename}'

        		content_list.append(f"{filename}.{ext}")

        		if not f"{filename}.{ext}" in dir_list:
            	if media_type == 1:
                download_file(PICTURE_DIR, media_url, filename, ext)
            elif media_type == 2:
                download_file(VIDEO_DIR, media_url, filename, ext)
            added = added + 1

    DIR = PICTURE_DIR if type in [0,1] else VIDEO_DIR

    print('>>')
    print(DIR)

    for file in dir_list:
        if not file in content_list:
            if os.path.exists(os.path.join(DIR, file)):
                os.remove(os.path.join(DIR, file))
                removed = removed + 1

    print(dir_list)
    print(content_list)

    if added > 0 or removed > 0:
        autorun.run(type)
        print(f'(+) Added {added} file(s)')
        print(f'(-) Removed {removed} file(s)')
    else:
        print('Already Updated!')
