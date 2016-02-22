import mechanize
import requests
from bs4 import BeautifulSoup as bs

def libgenSearch(book):
	name = book[0]
	author = book[1]
	url = "http://gen.lib.rus.ec/search.php?req="+name+" "+author+"&open=0&view=simple&phrase=1&column=def"
	source_code = requests.get(url)
	plain_text = source_code.text

	soup = bs(plain_text)
	table = soup.find('table', {'class':'c'})
	link = table.find('a', {'id':1})
	if link is None:
		return "None"

	url = "http://gen.lib.rus.ec/"+link['href']
	soup = bs(requests.get(url).text)
	table = soup.find('table')
	link = table.find('a')
	
	soup = bs(requests.get(link['href']).text)
	table = soup.find('table')
	link = table.find('a')
	return "http://libgen.io"+link['href']

def librarySearch(book):
	name = book[0]
	author = book[1]

	# br = mechanize.Browser()
	# br.set_handle_robots(False)
	url = "http://bidya.iitg.ernet.in:8680/opac/search/searchResult.html?searchdata="+name+"&qcon1=1&cat1=1&con1=1&searchdata2="+author+"&qcon2=1&cat2=0&con2=1&searchdata3=&qcon3=1&cat3=7&docType=BK&fromTF1=&toTF1=&sortBy=-1&level1=&physicalForm1=&sourceTF1=&subjectCode1=&subjectDocType1=&locationTF1=&db=8&databaseList=&search_selectedSites=1"
	source_code = requests.get(url)
	plain_text = source_code.text

	soup = bs(plain_text)

	# br.open(url)

	# nform = 0
	# for form in br.forms():
	# 	if str(form.attrs["id"]) == "searchForm":
	# 		br.select_form(nr = nform)
	# 	nform += 1

	# driver = webdriver.Firefox()
	# driver.wait = WebDriverWait(driver,0)

	# driver.get("http://bidya.iitg.ernet.in:8680/opac/")
	# link = driver.find_element_by_link_text('Advanced')
	# link.click()
	# x = driver.find_element_by_name("searchdata")
	# y = driver.find_element_by_name("searchdata2")
	# x.send_keys(name)
	# y.send_keys(author)
	# form = driver.find_element_by_id("searchForm")
	# form.submit()
	# source_code = requests.get("http://bidya.iitg.ernet.in:8680/opac/")
	# plain_text = source_code.text

	# soup = bs(plain_text)
	# print soup.find('a', {'id': 'Link167'})
	# for link in br.links():
	# 	print link.attrs[1]
	# 	if str(link.attrs[1]) == "Link66":
	# 		print link
	# 		print link.url
	# br.select_form(nr=0)
	# br.form["searchdata"] = "Digital Design"
	# br.form["cat1"] = ["1"]
	# br.click('a', {'id': 'Link167'})
	# br.form["searchdata2"] = "M Mano"
	# br.form["cat2"] = ["0"]
	# br["column"] = "title"
	# br.submit()
	# response = br.response().read()
	# test_file = open("test.html", "w")
	# test_file.write(str(soup))
	# print url