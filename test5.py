import mechanize
import cookielib
import urllib2
import json
from datetime import date
from bs4 import BeautifulSoup
import _mysql

url = "http://www.adm.uwaterloo.ca/infocour/CIR/SA/under.html"
page1 = urllib2.urlopen(url).read()
soup1 = BeautifulSoup(page1)
contents = [str(x.text) for x in soup1.find_all('option')]
courseNames = [contents[4].split()]
#print courseNames
data = []
counter =0
for cn in courseNames[0]:

 	if(cn != 'PD'):
		# Browser
		br = mechanize.Browser()

		# Cookie Jar
		cj = cookielib.LWPCookieJar()
		br.set_cookiejar(cj)

		# Browser options
		br.set_handle_equiv(True)
		br.set_handle_gzip(True)
		br.set_handle_redirect(True)
		br.set_handle_referer(True)
		br.set_handle_robots(False)

		# Follows refresh 0 but not hangs on refresh > 0
		br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

		# Want debugging messages?
		#br.set_debug_http(True)
		#br.set_debug_redirects(True)
		#br.set_debug_responses(True)

		# User-Agent (this is cheating, ok?)
		br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
		# Open some site, let's pick a random one, the first that pops in mind:
		r = br.open('http://www.adm.uwaterloo.ca/infocour/CIR/SA/under.html')
		html = r.read()
		#print html 
		#print br.title()
		fulltab=[]
		br.select_form(nr=0)

		 



		br.form['sess'] = ['1151',]
		br.form['subject']=[cn,]
		br.form['cournum'] = ''
		br.submit()
		count = 1
		page = br.response().read()
		soup = BeautifulSoup(page)
		table = soup.find('table',border = "2")
		if table != None:

			inner_table = table.find_all('table')

			for tab in inner_table:
				course = tab.previous.previous.previousSibling.previous.previous.previousSibling
				course_details = course.find_all('td')
				if len(course_details) == 1:
					 course = course.previous.previousSibling
					 course_details = course.find_all('td')
					 #print course_details

				
				rows = tab.find_all('tr')
				listtab=[]
				for  row in rows:
					t = row.find_all('td')
					dates = ""
					special = "NULL"

					if( (len(t) == 13) or (len(t) == 12) and t[1].string[0:3] != "TST") :
						
						listtab.append(t)
						# print t[10].next
						# if(t[10].next.next.name  == "br"):
						# 	print t[10].next.next.string 
						if(len(t[1].text) == 8):
							currentType = t[1].text[0:3]
						if(len(t[10].text) < 10):
							continue
						if(len(t[11].text) < 2):
							continue
						times = t[10].text.split("-")
						if(times[0] != "TBA"):
							counter+=1
							if(times[1].find("Th") != -1):
								times[1] = times[1].replace("Th","")
								dates = dates+"4"
							if(times[1].find("T") != -1):
								times[1] = times[1].replace("T","")
								dates = dates+"2"
							if(times[1].find("M") != -1):
								times[1] = times[1].replace("M","")
								dates = dates+"1"
							if(times[1].find("W") != -1):
								times[1] = times[1].replace("W","")
								dates = dates+"3"
							if(times[1].find("F") != -1):
								times[1] = times[1].replace("F","")
								dates = dates+"5"
							if(len(times[1]) > 5):
								special = times[1][2:].split("0",1)[1]
								special = special.replace("/","-")
								special = str(date.today().year)+"-"+special
							if(dates == ""):
								dates ="NULL"
							location = t[11].text.split(" ",1)
							building = location[0].strip()
							clsnum = location[1].strip()
							hourstr =int(times[0][0:2])
							hourend = int(times[1][0:2])
							firstName = "NULL"
							lastName = "NULL"
							if( (hourstr <= 7) ):
								hourstr +=12
								hourend += 12
								times[0] = times[0].replace(times[0][0:2],str(hourstr))
								times[1] = times[1].replace(times[1][0:2],str(hourend))
								
							if( (hourstr == 12) ):
								hourend += 12
								times[1] = times[1].replace(times[1][0:2],str(hourend))
							if(len(t) == 13):
								if(t[12].text.find(",") != -1):	
					 				names = t[12].text.split(",")
					 				firstName  = names[0]
					 				lastName = names[1].strip()
							print (str(course_details[0].string.strip()),str(course_details[1].string),str(currentType),(str(times[0]) + ":00"),(str(times[1])[0:5] + ":00"),str(special), str(building), str(clsnum),dates, str(firstName),str(lastName))
							info = {'Program': str(course_details[0].string.strip()),
									'coursenum': str(course_details[1].string),
									'type': str(currentType),
									'start': str(times[0]) + ":00",
									'end': str(times[1])[0:5] + ":00",
									'date': str(special),
									'building': str(building),
									'classNum': str(clsnum),
									'days': str(dates),
									'firstName': str(firstName),
									'lastName': str(lastName)
							}
							data.append(info)
							fulltab.append(listtab)

for a in data:
	print a
print json.dumps(data)

dataFile = open('../info.txt', 'w')
dataFile.write(json.dumps(data))
dataFile.close()

				

		




