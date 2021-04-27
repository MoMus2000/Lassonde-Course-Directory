from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import re
import matplotlib.pyplot as plt
import requests
import os
from treelib import Node, Tree
import json
import requests_cache
import difflib
from queue import PriorityQueue
requests_cache.install_cache('quick-lookUp',expire_after = 20000000)


option = Options()
option.add_argument("--log-level=3")
option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")
option.add_argument("--headless")


driver = webdriver.Chrome(executable_path='/Users/a./Desktop/lassonde/driver/chromedriver', options=option)

prog = ""

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
	program = input("Enter program name .. ")
	global prog
	prog = program
	# gloablprogram="Computer Science"
	try:
		driver.find_element_by_link_text(program).click()
	except Exception as e:
		pass
	time.sleep(2)
	print(driver.current_url)
	try:
		driver.find_element_by_xpath('//*[@id="ui-id-2"]').click()
	except Exception as e:
		pass
	time.sleep(2)
	try:
		driver.find_element_by_xpath('//*[@id="ui-id-6"]').click()
	except Exception as e:
		pass
	soup = BeautifulSoup(driver.page_source,'html.parser')
	faculty_name = soup.find('span',{"class" : "english"}).text
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
	global prog
	prog = program
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
	year = input("Enter accademic year eg 2018-2019 : ")
	if(year == ""):
		soup,faculty_name = current_year(driver)
	else:
		soup,faculty_name = previous_year(driver,year)
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
	tree.create_node(prog,"papa")
	for course in arr:
		num = comparator(course)
		if(num[0] == str(depth)):
			# print(course)
			tree.create_node(course,course,parent="papa")
			print(course)
			pre_reqs,hit1 = get_prerequisites(course)
			if(hit1 == False):
				time.sleep(4)
			for pre in pre_reqs:
				if(tree.get_node(course+""+pre) == None):
					tree.create_node(pre,course+""+pre,parent=course)
					pre2,hit2 = get_prerequisites(pre)
					if(hit2 == False):
						time.sleep(2)
					for pr in pre2:
						if(tree.get_node(course+""+pre+""+pr) == None):
							tree.create_node(pr,course+""+pre+""+pr,parent=course+""+pre)
							tests,hit3 = get_prerequisites(pr)
							if(hit3 == False):
								time.sleep(4)
							for tst in tests:
								if(tree.get_node(course+""+pre+""+pr+""+tst) == None):
									tree.create_node(tst,course+""+pre+""+pr+""+tst,parent=course+""+pre+""+pr)
	print("Still loading...")
	for course in arr:
		if(not tree.contains(course)):
			tree.create_node(course,course,parent="papa")
			pre_reqs,hit4 = get_prerequisites(course)
			if(hit4 == False):
				time.sleep(1)
			for pre in pre_reqs:
				if(tree.get_node(course+""+pre) == None):
					tree.create_node(pre,course+""+pre,parent=course)
					pre2,hit5 = get_prerequisites(pre)
					if(hit5 == False):
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
		# print(course_page.from_cache)
		# print(cn)
		soup = BeautifulSoup(course_page.text,'html.parser')
		soup_index = soup.text.rfind("Prerequisite")
		# print(soup_index)
		courses = soup.text[soup_index:-1].strip()
		pre_req2s = re.findall(regex_with_no_spaces,courses)
		if(len(pre_req2s) == 0):
			pre_req2s = re.findall(regex_with_spaces,courses)
		if(len(pre_req2s) == 0):
			pre_req2s = re.findall(regex_with_no_order,courses)
		# print(pre_req2s)
		return pre_req2s,course_page.from_cache
	except Exception as e:
		pass
	return [],False


def check_co_requisite(course_name):
	try:
		course_name = course_name.replace("/"," ")
		course_name = course_name + " 2020 FW"
		# print(course_name)
		regex_with_no_spaces = '[A-Z]{2}\/[A-Z]{4}\s*[0-9]{4} [0-9].00\s*(or [A-Z]{2}\/[A-Z]{4}\s*[0-9]{4} [0-9].00)*'
		# regex_with_spaces = '[A-Z]{2}\/[A-Z]{4} [0-9]{4} [0-9].00 (or [A-Z]{2}\/[A-Z]{4} [0-9]{4} [0-9].00)*'
		# regex_with_no_order = '[A-Z]+\d{4}'
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
		# print(courses)
		pre_req2s = re.finditer(regex_with_no_spaces,courses)
		courses = []
		for pre in pre_req2s:
			print(pre.group(0))
			prearray = pre.group(0).split("or")

		# if(len(pre_req2s) == 0):
		# 	pre_req2s = re.findall(regex_with_spaces,courses)
		# if(len(pre_req2s) == 0):
		# 	pre_req2s = re.findall(regex_with_no_order,courses)
		# print(pre_req2s.group(0))
		# print(pre_req2s.group(0))
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

	flag = True
	

	if(tree.contains(id_string) == True ):
		tree.remove_node(id_string)
	else:
		tree = contains_similar_id_prune(tree,id_string)
	os.system('cls' if os.name == 'nt' else 'clear')
	tree.show(line_type='ascii-emh')
			# if(names[8:12] == cour):
				# print(names)
	
	# print(courses)

def adding_to_tree(tree,arr):
	nodes = []
	tags = []
	for identifier in tree.all_nodes():
		tags.append(identifier.tag)
		nodes.append(identifier.identifier)
	tags = list(set(tags))
	nodes = list(set(nodes))
	courses_to_remove = input("Enter course hierarchy to remove (EG: 4101->2030->1300)..  \npress (r) for root")
	if(courses_to_remove.strip() == 'r'):
		course_name1 = input("Enter name")
		tree.create_node(course_name1,course_name1,parent=tree.root)

	else:	
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

		flag = True
		

		if(tree.contains(id_string) == True ):
			tree_name = input("Enter Tree branch Name: ")
			tree.create_node(tree_name,id_string+tree_name,parent=id_string)
		else:
			tree = contains_similar_id_add(tree,id_string)
	os.system('cls' if os.name == 'nt' else 'clear')
	tree.show(line_type='ascii-emh')



def contains_similar_id_add(tree,id_string):
	#Use difflib to get a close match to the id name
	nodes = tree.all_nodes()
	q = PriorityQueue()
	my_set = set()
	num2 = ''.join(filter(str.isdigit, id_string))
	for node in nodes:
		id_ = node.identifier
		num1 = ''.join(filter(str.isdigit, id_))
		seq=difflib.SequenceMatcher(None, num1,num2).ratio() 
		# print(seq)
		# print(seq)
		# print(id_string)
		if(seq > 0.1):
			my_set.add((-seq,id_,node.tag))
	
	for item in my_set:
		q.put(item)
	
	vals = []
	print("Top 10 matches")
	for i in range (0,11):
		next_item = q.get()
		print(f"{i}. {next_item[1]}")
		vals.append(next_item[1])

	value = input("Enter number to where add: ")
	# tree.remove_node(vals[int(value)])
	tree_name = input("Enter Tree branch Name: ")
	tree.create_node(tree_name,vals[int(value)]+tree_name,parent=vals[int(value)])

	return tree


def contains_similar_id_prune(tree,id_string):
	#Use difflib to get a close match to the id name
	nodes = tree.all_nodes()
	q = PriorityQueue()
	my_set = set()
	num2 = ''.join(filter(str.isdigit, id_string))
	for node in nodes:
		id_ = node.identifier
		num1 = ''.join(filter(str.isdigit, id_))
		seq=difflib.SequenceMatcher(None, num1,num2).ratio() 
		# print(seq)
		# print(seq)
		# print(id_string)
		if(seq > 0.1):
			my_set.add((-seq,id_,node.tag))
	
	for item in my_set:
		q.put(item)
	
	vals = []
	print("Top 10 matches")
	for i in range (0,11):
		next_item = q.get()
		print(f"{i}. {next_item[1]}")
		vals.append(next_item[1])

	value = input("Enter number to remove: ")
	tree.remove_node(vals[int(value)])

	return tree



def exporting_the_tree(tree,arr):
	# print(tree.all_nodes())
	# for f in tree.all_nodes():
	# 	print(tree.parent(f.identifier))
	print(arr)
	filename = input("Enter your filename: ")
	with open(f"{filename}.txt","w") as saves:
		for val in tree.all_nodes():
			if tree.parent(val.identifier) != None:
				s = ","+tree.parent(val.identifier).identifier
			else:
				s = ""
			saves.write(val.tag +","+ val.identifier + s)
			saves.write("\n")
		saves.write("END")
		saves.write("\n")
		for values in arr:
			# print(values)
			saves.write(str(values))
			# saves.write("\n")
	print("written the values")

def load_from_text(filepath):
	with open(filepath,"r") as saves:
		vals = saves.readlines()

	# print(vals)
	# tree.create_node(course,course,parent="papa")
	# tree.create_node(pr,course+""+pre+""+pr,parent=course+""+pre)
	tree = Tree()
	root = vals[0].split(",")
	root_name = root[0]
	root_id = root[1].rstrip("\n")
	tree.create_node(root_name,root_id)

	i =1
	for node in vals[1:]:
		print(node)
		if(node == "END\n"):
			index = i+1
			break
		split = node.split(",")
		name = split[0]
		tree_id = split[1].rstrip("\n")
		parent = split[2].rstrip("\n")
		i+=1
		tree.create_node(name,tree_id,parent=parent)
		# time.sleep(1)
	courses_array = []
	for line in range(i+1,len(vals)):
		courses_array.append(vals[line])

	os.system('cls' if os.name == 'nt' else 'clear')
	tree.show()
	print(f"Created tree from {i} nodes")
	return tree,courses_array




def main():
	os.system('cls' if os.name == 'nt' else 'clear')
	print("Created !")
	disk = input("Load from disk (d) ? ")
	if(disk == "d"):
		filepath = input("Please give absolute path :")
		tree,arr = load_from_text(filepath)
	else:
		tree,arr = get_academic_calenders(driver)
		with open("tree_json.txt","w") as f:
			f.write(tree.to_json())
		os.system('cls' if os.name == 'nt' else 'clear')
		tree.show()
	while(True):
		x = input("Save Tree (s) || Prune Tree (n) || Add (a) || Quit (q)")
		if(x=="n"):
			pruning_the_tree(tree,arr)
		if(x == "s"):
			exporting_the_tree(tree,arr)
		if(x == "a"):
			adding_to_tree(tree,arr)
		if(x == "q"):
			break
	# vals = check_co_requisite("LE/EECS 2030 3")
	# print(vals)
	return
			
main()

