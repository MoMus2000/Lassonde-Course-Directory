from bs4 import BeautifulSoup
import requests
import os
import re
# az = "FW"
# fc = "LE"
# sb = "EECS"
# ay = "2020"
# cn = "2030"
# cr = "3.00"

hardcoded_faculty_names = ['AK','AP','AS','ED','ES','EU','FA','GL','GS','HH','LE','LW','SB','SC']

regex_with_no_spaces = '[A-Z]{2}\/[A-Z]{4} [0-9]{4} [0-9].00'
regex_with_spaces = '[A-Z]{2}\/ [A-Z]{4} [0-9]{4} [0-9].00'

while(True):
	print("----------------------------------------------------------------------------")
	# print("\n")
	input_str = input("Faculty Subject CourseNumber CourseCredit AccademicYear Term \nEg->(LE EECS 2031 3 2020 FW)\n")
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
		pre_req_list1 = re.findall(regex_with_spaces,course_description[3].text[pre_req:pre_req2])
		pre_req_list2 = re.findall(regex_with_no_spaces,course_description[3].text[pre_req:pre_req2])
		# pre_req_list = list(dict.fromkeys(pre_req_list))
		# print(pre_req_list1)
		# print(pre_req_list2)
		
		inp = input("Would you like to check out the PreReqs y/n ?")
		if(inp == 'y' or inp == 'Y'):
			i = 0
			for course in pre_req_list2:
				print(str(i)+". "+course)
				i+=1
			#Call function again on the inputs after preparing them for execution
			#Strip down the ugly code and pls make it cleaner
		else:
			pass
			#Return back to the execution
