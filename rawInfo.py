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


#get every option of course from options 
data = []  #saving lectures info 
courseData =[] #saving course info 
buildingData = []
counter =0
# <-- accessing browser and website  -->
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

		 


# <-- accessing the school schecule of classes website and getting data fr every course in the school  -->
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
# 					 courseInfo = {'Program': str(course_details[0].string.strip()),
#  							'coursenum': str(course_details[1].string),
# 							'courseName': str(course_details[3].string)
# 								 }
# 					 courseData.append(courseInfo)
	


# <-- getting data about lectures  -->
				
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
					
							hourstr =int(times[0][0:2])
							hourend = int(times[1][0:2])
							addy = t[11].text
							clsnum = ""
							building = ""
							if(addy.find(" ") != -1):
								location = t[11].text.split(" ",1)
								building = location[0].strip()
								clsnum = location[1].strip()

							else:
								location = addy.split("U")
								building = location[0].strip()+"U"
								clsnum = location[1].strip()
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
							#print (str(course_details[3].string),str(course_details[0].string.strip()),str(course_details[1].string),str(currentType),(str(times[0]) + ":00"),(str(times[1])[0:5] + ":00"),str(special), str(building), str(clsnum),dates, str(firstName),str(lastName))
							info = {'Program': str(course_details[0].string.strip()),
									'coursenum': str(course_details[1].string),
									'courseName': str(course_details[3].string),
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

var = {'courseTitle': data[0]["Program"],
 	    'courseNumber': data[0]["coursenum"],
 		'courseDesc': data[0]["courseName"]
 		   }

courseData.append(var)


var2 = data[0]['building']
buildingData.append(var2)

# <-- getting the building info  -->
for a in data:
	if a['building'] in buildingData:
		pass
	else:
		buildingData.append(a['building'])

#print buildingData

# <-- getting the course data which in coursetitle,coursenum,coursename  -->
for a in data:

	if(a["courseName"] != var['courseDesc']):
		info2 = {'courseTitle': a["Program"],
		   			 'courseNumber': a["coursenum"],
		   			 'courseDesc': a["courseName"],
					}
		courseData.append(info2)
		var = info2


#print json.dumps(data)
progNames=[]
progInfo =[]
var5 = { 'ProgramDesc':data[0]['Program'],
		'ProgramID':  100000
		
}
var6 = data[0]['Program']
progNames.append(var6)
progInfo.append(var5)
count = 1
for a in data:
	
	if a['Program'] not in progNames:
		info = {'ProgramDesc':a['Program'],
				'ProgramID':  100000 + count
				}
		count += 1
		progInfo.append(info)
		progNames.append(a['Program'])

courseNames =[]
courseInfo = []
var7 = { 'CourseID': 200000,
		'ProgramID': progInfo[0]['ProgramID'],
		'courseName': data[0]['coursenum'],
		'courseDesc': data[0]['courseName']}
var8 = {'program': data[0]['Program'],
		'Coursename': data[0]['coursenum']}
courseNames.append(var8)
courseInfo.append(var7)
count2 = 1
for  a in progNames:
	for b in data:
		test ={ 'program': b['Program'],
				'Coursename': b['coursenum']
		}

		if test not in courseNames:
			for c in progInfo:
				if c['ProgramDesc'] == b['Program']:
					info = {'CourseID': 200000 + count2,
						'ProgramID':  c['ProgramID'],
						'courseName': b['coursenum'],
						'courseDesc': b['courseName']
					}
					count2 += 1
					courseNames.append(test)
					courseInfo.append(info)



#<-- checking data of class before before adding to file  -->
#print json.dumps(courseData)


buildingRooms = []
var3 = data[0]['classNum']
roomNumber = {'building': buildingData[0],
			  'roomNum': var3
			 }

buildingRooms.append(roomNumber)
for a in buildingData:
	roomNumbers =[]
	roomNumbers.append(var3)
	for b in data:
		if (a == b['building']):
			if(b['classNum'] in roomNumbers):
				pass
			else:
				roomNumbers.append(b['classNum'])
				room = {'building': a,
						'roomNum': b['classNum']
						}
				buildingRooms.append(room)

#print buildingRooms
# for a in data:
# 	print a
mondayclassRoomsUsage =[]
for a in buildingRooms:
	times = []
	for b in data:
		if(b['building'] == a['building'] and b['classNum'] == a['roomNum'] ):
			if("1" in b['days'] ):
				time = {'endTime': b['end'],
						'startTime': b['start']
				}
				if time in times:
					pass
				else:
					times.append(time)
					times =sorted(times, key=lambda k: k['startTime'])


	var4 = { 'buiding': a['building'],
			'roomNumb': a['roomNum'],
			'times': times,
			'day': 1
	}
	if (times== []):
		pass
	else:
		mondayclassRoomsUsage.append(var4)	
# print "\n"
# print "MONDAY"
# print "\n"	
# print mondayclassRoomsUsage	


tuesdayclassRoomsUsage =[]
for a in buildingRooms:
	times = []
	for b in data:
		if(b['building'] == a['building'] and b['classNum'] == a['roomNum'] ):
			if("2" in b['days'] ):
				time = {'endTime': b['end'],
						'startTime': b['start']
				}
				if time in times:
					pass
				else:
					times.append(time)
					times =sorted(times, key=lambda k: k['startTime'])


	var4 = { 'buiding': a['building'],
			'roomNumb': a['roomNum'],
			'times': times,
			'day': 2
	}
	if (times== []):
		pass
	else:
		tuesdayclassRoomsUsage.append(var4)
	

wedclassRoomsUsage =[]
for a in buildingRooms:
	times = []
	for b in data:
		if(b['building'] == a['building'] and b['classNum'] == a['roomNum'] ):
			if("3" in b['days'] ):
				time = {'endTime': b['end'],
						'startTime': b['start']
				}
				if time in times:
					pass
				else:
					times.append(time)
					times =sorted(times, key=lambda k: k['startTime'])


	var4 = { 'buiding': a['building'],
			'roomNumb': a['roomNum'],
			'times': times,
			'day': 3
	}
	if (times== []):
		pass
	else:
		wedclassRoomsUsage.append(var4)
# print "\n\n\n"
# print "WEDNESDAY"
# print "\n"
# print wedclassRoomsUsage	

thuclassRoomsUsage =[]
for a in buildingRooms:
	times = []
	for b in data:
		if(b['building'] == a['building'] and b['classNum'] == a['roomNum'] ):
			if("4" in b['days'] ):
				time = {'endTime': b['end'],
						'startTime': b['start']
				}
				if time in times:
					pass
				else:
					times.append(time)
					times =sorted(times, key=lambda k: k['startTime'])


	var4 = { 'buiding': a['building'],
			'roomNumb': a['roomNum'],
			'times': times,
			'day': 4
	}
	if (times== []):
		pass
	else:
		thuclassRoomsUsage.append(var4)
# print "\n\n\n"
# print "THURSDAY"
# print "\n"
# print thuclassRoomsUsage	

friclassRoomsUsage =[]
for a in buildingRooms:
	times = []
	for b in data:
		if(b['building'] == a['building'] and b['classNum'] == a['roomNum'] ):
			if("5" in b['days'] ):
				time = {'endTime': b['end'],
						'startTime': b['start']
				}
				if time in times:
					pass
				else:
					times.append(time)
					times =sorted(times, key=lambda k: k['startTime'])


	var4 = { 'buiding': a['building'],
			'roomNumb': a['roomNum'],
			'times': times,
			'day': 5
	}
	if (times== []):
		pass
	else:
		friclassRoomsUsage.append(var4)
# print "\n\n\n"
# print "FRIDAY"
# print "\n"
# print friclassRoomsUsage	

print buildingData
allclassInfo = []
allclassInfo.append(mondayclassRoomsUsage)
allclassInfo.append(tuesdayclassRoomsUsage)
allclassInfo.append(wedclassRoomsUsage)
allclassInfo.append(thuclassRoomsUsage)
allclassInfo.append(friclassRoomsUsage)

#print allclassInfo
#<-- Adding the JSON data about  lectureto lecture.txt -->
# dataFile = open('/Applications/MAMP/htdocs/Class/lecture.txt', 'w')
# dataFile.write(json.dumps(data))
# dataFile.close()

# # <-- Adding the JSON data about courses to class.txt -->
# dataFile = open('/Applications/MAMP/htdocs/Class/courses.txt', 'w')
# dataFile.write(json.dumps(courseData))
# dataFile.close()
			
# #<-- Adding the JSON data about buildings to building.txt -->
# dataFile = open('/Applications/MAMP/htdocs/Class/building.txt', 'w')
# dataFile.write(json.dumps(buildingData))
# dataFile.close()

# # <-- Adding the JSON data about class times for each day to allclassInfo.txt -->
# dataFile = open('/Applications/MAMP/htdocs/Class/allclassInfo.txt', 'w')
# dataFile.write(json.dumps(allclassInfo))
# dataFile.close()

# # <-- Adding the JSON data about class times for each day to allclassInfo.txt -->
# dataFile = open('/Applications/MAMP/htdocs/Class/program.txt', 'w')
# dataFile.write(json.dumps(progInfo))
# dataFile.close()


	
