import requests
from bs4 import BeautifulSoup
from webcrawler import showBooks





def stripAll(text):
	strippedText = ''.join(text.split())
	return strippedText

def splitAndJoin(text):
	return " ".join(text.split()).rstrip().lstrip()

def removeSpaces(text):
	return "".join(text.split()).rstrip().lstrip()

def getDate(rows,j):
	ans=rows[j].find('td')
	b=splitAndJoin(ans.text)
	a=b.split()
	return a[4]


def findDate(rows,i):
	j=i

	while j>0:
		if 'Day' in rows[j].text:
			return getDate(rows,j)
		else:	
			j=j-1

def getRoom(course,rows,i):
	columns=rows[i].findAll('td')
	
	for i in range(len(columns)):
		text=columns[i].text
		if course in text:
			start=text.index('(',text.index(course)+ len(course)-1)
			end=text.index(')',text.index(course)+ len(course)-1)
			return text[start+1:end]



def examtt(courses):
	url = "http://shilloi.iitg.ernet.in/~acad/intranet/tt/ett.htm"
	source_code = requests.get(url)
	plain_text = source_code.text

	soup = BeautifulSoup(plain_text,"lxml")
	table = soup.findAll('table', {'class':'MsoNormalTable'})
	date=[]
	rooms=[]
	sortcourse=[]

	for k in range(len(table)):
		rows=table[k].findAll('tr')
		for j in range(len(courses)):
			for i in range(len(rows)):
				text=rows[i].text
				if courses[j] in text:
					date.append(findDate(rows,i))
					rooms.append(getRoom(courses[j],rows,i))
					sortcourse.append(courses[j])
					break
				
	listarr = []				
	for i in range(len(date)):
		item = [sortcourse[i] ,removeSpaces(date[i]) ,removeSpaces(rooms[i])]
		listarr.append(item)
	return listarr	



def listTT(dept,sem):
	courses = showBooks(dept, sem,"courses")
	coursecodes = []
	for course in courses:
		# print course
		code=course[0]
		depc = code[0:2]
		ccode = code[2:]
		finalc = depc+" "+ccode	
		if finalc != " ":
			coursecodes.append(finalc)
	coursecodes=list(set(coursecodes))


	# print coursecodes
	return examtt(coursecodes)	


# print listTT("CSE",4)

# examtt(['CS 201','CS 202','EE 230','CS 204'])