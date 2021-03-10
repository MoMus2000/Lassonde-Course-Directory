from bs4 import BeautifulSoup
import requests


# az = "FW"
# fc = "LE"
# sb = "EECS"
# ay = "2020"
# cn = "2030"
# cr = "3.00"





while(True):
	print("-----------------")
	# print("\n")
	input_str = input("Faculty Subject CourseNumber CourseCredit AccademicYear Term \n")
	splits = input_str.split(" ")

	fc = splits[0].upper()
	sb = splits[1].upper()
	cn = splits[2]
	cr = float(splits[3]) #2 dp for float
	ay = splits[4]
	az = splits[5].upper()
	york_url = f"https://w2prod.sis.yorku.ca/Apps/WebObjects/cdm.woa/wa/crsq?fa={fc}&sj={sb}&cn={cn}&cr={cr}&ay={ay}&ss={az}"
	# print(york_url)

	req = requests.get(york_url)
	# print(req.text)
	soup = BeautifulSoup(req.text,'html.parser')


	heading = soup.find_all('p',{"class":"heading"})
	course_description_title = soup.find_all('strong')
	course_description = soup.find_all('p')
	print(heading[0].text)
	pre_req = course_description[3].text.find("Prerequisite")
	# print(pre_req)
	print(course_description_title[0].text)
	print(course_description[3].text[0:pre_req])
	if( pre_req == -1):
		print("No Prerequisites for this course")
	else:
		pre_req2 = course_description[3].text.find(". ",pre_req+1)
		# date_remove =course_description[3].text.find("Date",pre_req+1)
		print(course_description[3].text[pre_req:pre_req2])
	print("-----------------")
