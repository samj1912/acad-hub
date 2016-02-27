import requests
from bs4 import BeautifulSoup
from webcrawler import showCourses


#functions to remove spaces as desired
def stripAll(text):
	strippedText = ''.join(text.split())
	return strippedText

def splitAndJoin(text):
	return " ".join(text.split()).rstrip().lstrip()

def removeSpaces(text):
	return "".join(text.split()).rstrip().lstrip()

#function to get date from the first column
def getDate(rows,j):
	ans=rows[j].find('td')			#getting text of the first column of the row
	b=splitAndJoin(ans.text)
	a=b.split()						#splitting text by spaces
	return a[4]						#returning 5th index of the array

#function to find date
def findDate(rows,i):
	j=i
	while j>0:						#iterating backward through the rows
		if 'Day' in rows[j].text:	#checking i day is present in the row's text
			return getDate(rows,j)	
		else:	
			j=j-1

#function to find the room of the course exam
def getRoom(course,rows,i):
	columns=rows[i].findAll('td')			#finding all columns in that particular row
	
	for i in range(len(columns)):			#iterating through all columns
		text=columns[i].text                #storing the text of the column in a variable
		if course in text:					#checking if the course is present in text
			start=text.index('(',text.index(course)+ len(course)-1) 	#finding the index of the first ( that appears after the course in text
			end=text.index(')',text.index(course)+ len(course)-1)		#finding the index of the first ) that appears after the course in text 
			return text[start+1:end]		#returning the string in between the two indices



def examtt(courses):
	url = "http://shilloi.iitg.ernet.in/~acad/intranet/tt/ett.htm"
	source_code = requests.get(url)
	plain_text = source_code.text

	soup = BeautifulSoup(plain_text,"lxml")						#using BS4 to parse the text
	table = soup.findAll('table', {'class':'MsoNormalTable'})	#finding all tables in the html file
	date=[]
	rooms=[]
	sortcourse=[]

	for k in range(len(table)):					#iterating through all tables of the file
		rows=table[k].findAll('tr')				#finding all rows of the particular table
		for j in range(len(courses)):	
			for i in range(len(rows)):				
				text=rows[i].text               #storing the text of row in a variable
				if courses[j] in text:			#finding if the course is present in the text
					date.append(findDate(rows,i))					#calling finddate function and appending it in the date array
					rooms.append(getRoom(courses[j],rows,i))		#calling findroom function and appending it in the room array
					sortcourse.append(courses[j])					#appending course in course array
					break
				
	listarr = []								
	for i in range(len(date)):					
		item = [sortcourse[i] ,removeSpaces(date[i]) ,removeSpaces(rooms[i])]  #making a item of each course
		listarr.append(item)					#appending it to the list array
	return listarr	



def listTT(dept,sem):
	courses = showCourses(dept, sem)     #gets courses of the dep and sem from the webcrawler file
	coursecodes = []
	for course in courses:				#iterating through each course in courses array
		# print course
		code=course[0]					
		depc = code[0:2]
		ccode = code[2:]
		finalc = depc+" "+ccode	
		if finalc != " ":
			coursecodes.append(finalc)	#getting the course code in the appropriate format for function
	coursecodes=list(set(coursecodes))


	# print coursecodes
	return examtt(coursecodes)	


# print listTT("CSE",4)

# examtt(['CS 201','CS 202','EE 230','CS 204'])