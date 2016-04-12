import requests

def uploadFile(file):
	url = 'http://10.0.2.22/upload.php'
	files = {'fileToUpload': open(file, 'rb')}
	r = requests.post(url, files=files)
	return r.text