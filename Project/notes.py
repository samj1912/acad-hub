import requests
import os

def uploadFile(file, roll, course):
	url = 'http://10.0.2.22/upload.php'
	files = {'fileToUpload': open(file, 'rb')}
	data = {'roll':roll, 'course':course}
	r = requests.post(url, files=files, data=data)
	if r.text == "Ok":
		print "Your file has been uploaded successfully!"
	else:
		print "error"

def listUploads(course):
	url = 'http://10.0.2.22/listfiles.php'
	data = {'course':course}
	r = requests.post(url, data=data)
	files = r.text.split("\n")[:-1]
	icondir = 'icons/'
	fileicons = os.listdir(icondir)
	uploadedby = []
	filename = []
	icons = []
	for i in files:
		uploadedby.append(i[:9])
		filename.append(i[9:])
		flag = 0
		for icon in fileicons:
			if i.split('.')[-1] in icon.split('.')[0]:
				flag = 1
				icons.append(icondir+icon)
				break
		if flag is 0:
			icons.append(icondir+'default.png')
	return icons, filename, uploadedby


# listUploads("CS203")
# uploadFile('exam.py')