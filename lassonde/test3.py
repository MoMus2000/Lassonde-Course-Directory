from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import re
import matplotlib.pyplot as plt
import requests
from treelib import Node, Tree
import json

option = Options()
option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")
option.add_argument("--headless")

driver = webdriver.Chrome(ChromeDriverManager().install(), options=option)


Faculties = {
	'Faculty of Science' : 'SC',
	'Lassonde School of Engineering' : 'LE',
	'Faculty of Liberal Arts and Professional Studies': 'AP',
	'Faculty of Environmental Studies': 'ES',
	'Faculty of Arts' : 'AS',
	'Faculty of Education' : 'ED',
	'Faculty of Environmental and Urban Change': 'EU',
	'School of the Arts, Media, Performance and Design' : 'FA',
	'Glendon College':'GL',
	'Faculty of Health': 'HH',
	'Osgoode Hall Law School' : 'LW',
	'Schulich School of Business' : 'SB'
}

def list_subjects(driver):
	url = 'https://calendars.students.yorku.ca/'
	driver.get(url)
	soup = BeautifulSoup(driver.page_source, 'html.parser')
	for heading in soup.find_all('h1'):
		print(heading.text)


def current_year(driver):
	url = 'https://calendars.students.yorku.ca/'
	driver.get(url)
	# program = input("Enter program name .. ")
	program="Computer Science"
	driver.find_element_by_link_text(program).click()
	time.sleep(2)
	print(driver.current_url)
	driver.find_element_by_xpath('//*[@id="ui-id-2"]').click()
	time.sleep(2)
	driver.find_element_by_xpath('//*[@id="ui-id-6"]').click()
	soup = BeautifulSoup(driver.page_source,'html.parser')
	faculty_name = soup.find('span',{"class" : "english"}).text
	# print(driver.page_source)
	# //*[@id="ui-id-6"]
	# try:
	# 	driver.find_element_by_xpath('//*[@id="ui-id-2"]').click()
	# except Exception as e:
	# 	print("Degree requirements not found")
	# time.sleep(2)
	# try:
	# 	driver.find_element_by_xpath('//*[@id="program_degree_requirements_english_heading"]').click()
	# except Exception as e:
	# 	try:
	# 		driver.find_element_by_xpath('//*[@id="ui-id-6"]/span[1]').click()
	# 	except Exception as e:
	# 		print("No degree requirements have been found ..")
	return soup,faculty_name


def previous_year(driver,year):
	url = 'https://calendars.students.yorku.ca/2020-2021/previous-undergraduate-calendars'
	driver.get(url)
	# year = input("Enter accademic year eg 2018-2019 : ")
	regex = "\d{4}"
	years = re.findall(regex, year)
	if(len(years) != 2):
		pass
	year_string = f"Undergraduate Calendar {years[0]}-{years[1]}"
	# soup = BeautifulSoup(driver.page_source, 'html.parser')
	driver.find_element_by_link_text(year_string).click()
	program = input("Enter program name .. ")
	# program = "Computer Science"
	driver.find_element_by_link_text(program).click()
	time.sleep(2)
	print(driver.current_url)
	try:
		driver.find_element_by_xpath('//*[@id="degree_requirements_english_heading"]').click()
	except Exception as e:
		print("Degree requirements not found")
	time.sleep(2)
	try:
		driver.find_element_by_xpath('//*[@id="program_degree_requirements_english_heading"]').click()
	except Exception as e:
		try:
			driver.find_element_by_xpath('//*[@id="ui-id-6"]/span[1]').click()
		except Exception as e:
			print("No degree requirements have been found ..")
	# print(driver.page_source)
	soup = BeautifulSoup(driver.page_source,'html.parser')
	faculty_name = soup.find('h2',{"class" : "page__title title english"}).text

	return soup,faculty_name



def get_academic_calenders(driver):
	# url = 'https://calendars.students.yorku.ca/2020-2021/previous-undergraduate-calendars'
	# driver.get(url)
	year = input("Enter accademic year eg 2018-2019 : ")
	if(year == ""):
		soup,faculty_name = current_year(driver)
		# a()
	# year = "2018 2019"
	else:
		soup,faculty_name = previous_year(driver,year)
	# 	regex = "\d{4}"
	# 	years = re.findall(regex, year)
	# 	if(len(years) != 2):
	# 		pass
	# 	year_string = f"Undergraduate Calendar {years[0]}-{years[1]}"
	# 	# soup = BeautifulSoup(driver.page_source, 'html.parser')
	# 	driver.find_element_by_link_text(year_string).click()
	# 	program = input("Enter program name .. ")
	# 	# program = "Computer Science"
	# 	driver.find_element_by_link_text(program).click()
	# 	time.sleep(2)
	# 	print(driver.current_url)
	# 	try:
	# 		driver.find_element_by_xpath('//*[@id="degree_requirements_english_heading"]').click()
	# 	except Exception as e:
	# 		print("Degree requirements not found")
	# 	time.sleep(2)
	# 	try:
	# 		driver.find_element_by_xpath('//*[@id="program_degree_requirements_english_heading"]').click()
	# 	except Exception as e:
	# 		try:
	# 			driver.find_element_by_xpath('//*[@id="ui-id-6"]/span[1]').click()
	# 		except Exception as e:
	# 			print("No degree requirements have been found ..")
	# # print(driver.page_source)
	# 	soup = BeautifulSoup(driver.page_source,'html.parser')
	# 	faculty_name = soup.find('h2',{"class" : "page__title title english"}).text
	# print(soup)
	regex = f"{Faculties[faculty_name]}\D[a-zA-Z]{{4}} \d{{4}} \d"
	print(regex)
	courses = re.findall(regex,soup.text)
	print(set(courses))
	arr = sorted(set(courses))
	arr.sort(key = comparator)
	tree = create_tree(arr)
	return tree
	# tree.show()
  	
	#Start looking at degree types and filter out information on those basis


def comparator(courses):
	regex = '\d{4}'
	lis = re.findall(regex,courses)
	# print(lis[0])
	return lis[0]

def create_tree(arr,depth='4'):
	tree = Tree()
	print("creating your tree ..")
	# print(tree.get_node("compsci"))
	tree.create_node("compsci","papa")
	for course in arr:
		num = comparator(course)
		if(num[0] == str(depth)):
			# print(course)
			tree.create_node(course,course,parent="papa")
			pre_reqs = get_prerequisites(course)
			time.sleep(1)
			for pre in pre_reqs:
				if(tree.get_node(course+""+pre) == None):
					tree.create_node(pre,course+""+pre,parent=course)
					pre2 = get_prerequisites(pre)
					time.sleep(1)
					for pr in pre2:
						if(tree.get_node(course+""+pre+""+pr) == None):
							tree.create_node(pr,course+""+pre+""+pr,parent=course+""+pre)
							tests = get_prerequisites(pr)
							time.sleep(1)
							for tst in tests:
								if(tree.get_node(course+""+pre+""+pr+""+tst) == None):
									tree.create_node(tst,course+""+pre+""+pr+""+tst,parent=course+""+pre+""+pr)
	print("Still loading...")
	for course in arr:
		if(not tree.contains(course)):
			tree.create_node(course,course,parent="papa")
			pre_reqs = get_prerequisites(course)
			time.sleep(1)
			for pre in pre_reqs:
				if(tree.get_node(course+""+pre) == None):
					tree.create_node(pre,course+""+pre,parent=course)
					pre2 = get_prerequisites(pre)
					time.sleep(1)
				
	return tree,arr



#Fix the credit value issue that affects removal by id
#Clean the code and merge with the main file

def get_prerequisites(course_name):
	try:
		course_name = course_name.replace("/"," ")
		course_name = course_name + " 2020 FW"
		# print(course_name)
		regex_with_no_spaces = '[A-Z]{2}\/[A-Z]{4} [0-9]{4} [0-9].00'
		regex_with_spaces = '[A-Z]{2}\/ [A-Z]{4} [0-9]{4} [0-9].00'
		regex_with_no_order = '[A-Z]+\d{4}'
		splits = course_name.split(" ")
		# print(splits)
		fc = splits[0]
		sb = splits[1]
		cn = splits[2]
		cr = float(splits[3])
		ay = splits[4]
		az = splits[5]
		york_url = f"https://w2prod.sis.yorku.ca/Apps/WebObjects/cdm.woa/wa/crsq?fa={fc}&sj={sb}&cn={cn}&cr={cr}&ay={ay}&ss={az}"
		course_page = requests.get(york_url)
		soup = BeautifulSoup(course_page.text,'html.parser')
		soup_index = soup.text.rfind("Prerequisite")
		courses = soup.text[soup_index:-1].strip()
		pre_req2s = re.findall(regex_with_no_spaces,courses)
		if(len(pre_req2s) == 0):
			pre_req2s = re.findall(regex_with_spaces,courses)
		if(len(pre_req2s) == 0):
			pre_req2s = re.findall(regex_with_no_order,courses)
		return pre_req2s
	except Exception as e:
		pass
	return []


def pruning_the_tree(tree,arr):
	# print(arr[0][7:11])
	nodes = []
	tags = []
	for identifier in tree.all_nodes():
		tags.append(identifier.tag)
		nodes.append(identifier.identifier)
	tags = list(set(tags))
	nodes = list(set(nodes))
	courses_to_remove = input("Enter course hierarchy to remove (EG: 4101->2030->1300) \n")
	courses = courses_to_remove.split("->")

	# print(tags[0][8:12] + " PRINTTTTTT")
	id_string =""
	visted = []
	for tag in tags:
		for i in range(0,len(courses)):
			if(tag[8:12] == courses[i] and tag[8:12] not in visted):
				print(tag)
				courses[i] = tag
				# id_string= id_string+tag
		visted.append(tag[8:12])
	print(courses)
	id_string = ""
	for course in courses:
		id_string = id_string+course
	print(id_string)

	if(tree.contains(id_string) == True ):
		tree.remove_node(id_string)


	tree.show(line_type='ascii-emh')
	# 		if(names[8:12] == cour):
	# 			print(names)
	
	# print(courses)

def main():
	print("Created !")
	tree,arr = get_academic_calenders(driver)
	with open("tree_json.txt","w") as f:
		f.write(tree.to_json())
	# tree.show()

	while(True):
		x = input("Does the tree look good...? (y/n)")
		if(x=="n"):
			# input_id = input("Enter tree id")
			pruning_the_tree(tree,arr)
			# tree.remove_node(input_id)
			# tree.show(line_type="ascii-em")

	# print("Completed Creating your tree..")
	# while(True):
main()

