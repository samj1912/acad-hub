import requests
import os

def uploadFile(file):
	url = 'http://10.0.2.22/upload.php'
	files = {'fileToUpload': open(file, 'rb')}
	r = requests.post(url, files=files)
	return r.text


def listUploads():
	files = os.listdir('.')
	fileicon = 'pdficon.png'
	x = []
	for i in files:
		x.append(fileicon)
	return x, files


# listUploads()