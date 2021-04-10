from treelib import Tree,Node
import re
import requests
from bs4 import BeautifulSoup
import time

arr = ['LE/EECS 4090 6', 'LE/EECS 3911 3', 'LE/EECS 4111 3', 'LE/EECS 2011 3', 
'LE/COOP 3109 0', 'LE/EECS 1019 3', 'LE/EECS 4313 3', 'LE/EECS 3401 3', 
'LE/EECS 2910 3', 'LE/EECS 1028 3', 'LE/EECS 3221 3', 'LE/COOP 2109 0', 
'LE/EECS 3910 3', 'LE/EECS 4911 3', 'LE/EECS 1012 3', 'LE/COOP 3100 2', 
'LE/EECS 1022 3', 'LE/EECS 2021 4', 'LE/EECS 2031 3', 'LE/EECS 2311 3', 
'LE/EECS 3215 4', 'LE/EECS 3101 3', 'LE/EECS 2001 3', 'LE/EECS 3461 3', 
'LE/EECS 1001 1', 'LE/EECS 4115 3', 'LE/EECS 2030 3', 'LE/COOP 2100 2', 
'LE/EECS 1911 3', 'LE/EECS 4088 6', 'LE/EECS 1710 3', 'LE/EECS 4910 3', 
'LE/EECS 2911 3', 'LE/EECS 1720 3', 'LE/EECS 4312 3', 'LE/EECS 4101 3', 
'LE/EECS 3000 3', 'LE/EECS 1910 3', 'LE/EECS 3311 3', 'LE/EECS 3421 3', 
'LE/EECS 3342 3']
# arr = ['LE/EECS 1011 3', 'LE/ESSE 1012 3', 'LE/EECS 1019 3', 'LE/EECS 1021 3',
#  'LE/EECS 1028 3', 'LE/MECH 2112 3', 'LE/MECH 2201 3', 'LE/MECH 2202 3', 'LE/ESSE 2210 3',
#   'LE/MECH 2301 3', 'LE/MECH 2302 3', 'LE/MECH 2401 3', 'LE/MECH 2412 3', 'LE/MECH 2502 3', 
#   'LE/MECH 3201 3', 'LE/MECH 3202 3', 'LE/MECH 3203 3', 'LE/MECH 3302 3', 'LE/MECH 3401 3', 
#   'LE/MECH 3409 3', 'LE/MECH 3502 3', 'LE/MECH 3503 3', 'LE/MECH 3504 3', 'LE/EECS 3505 3', 
#   'LE/MECH 4201 3', 'LE/MECH 4401 3', 'LE/MECH 4402 4', 'LE/MECH 4502 3', 'LE/MECH 4504 3', 'LE/MECH 4510 3']


def comparator(courses):
	regex = '\d{4}'
	lis = re.findall(regex,courses)
	# print(lis[0])
	return lis[0]

def get_prerequisites(course_name):
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
	# print(york_url)
	course_page = requests.get(york_url)
	soup = BeautifulSoup(course_page.text,'html.parser')
	# pre_reqs = re.findall(regex_with_spaces,soup.text)
	soup_index = soup.text.rfind("Prerequisite")
	courses = soup.text[soup_index:-1].strip()
	# print(courses)
	# print(courses)
	pre_req2s = re.findall(regex_with_no_spaces,courses)
	if(len(pre_req2s) == 0):
		pre_req2s = re.findall(regex_with_spaces,courses)
	if(len(pre_req2s) == 0):
		pre_req2s = re.findall(regex_with_no_order,courses)
	return pre_req2s


def create_tree(arr):
	tree = Tree()
	print("creating your tree ..")
	print(tree.get_node("compsci"))
	tree.create_node("compsci","papa")
	for course in arr:
		num = comparator(course)
		if(num[0] == '4'):
			print(course)
			tree.create_node(course,course,parent="papa")
			pre_reqs = get_prerequisites(course)
			time.sleep(1)
			for pre in pre_reqs:
				if(tree.get_node(pre) == None):
					tree.create_node(pre,course+""+pre,parent=course)
					pre2 = get_prerequisites(pre)
					time.sleep(1)
					for pr in pre2:
						if(tree.get_node(pr) == None):
							tree.create_node(pr,course+""+pre+""+pr,parent=course+""+pre)
							tests = get_prerequisites(pr)
							time.sleep(1)
							for tst in tests:
								if(tree.get_node(tst) == None):
									tree.create_node(tst,course+""+pre+""+pr+""+tst,parent=course+""+pre+""+pr)
	return tree




# print("OK 123")
# for course in arr:
#     if(not tree.contains(course)):
#         tree.create_node(course,course,parent="papa")
#         pre_reqs = get_prerequisites(course)
#         time.sleep(1)
#         for pre in pre_reqs:
#             if(tree.get_node(pre) == None):
#                 tree.create_node(pre,course+""+pre,parent=course)
#                 pre2 = get_prerequisites(pre)
#                 time.sleep(1)

# for course in arr:
#     num = comparator(course)
#     # print(num)
#     if(num[0] == '3'):
#     	# print("We are jhere")
#     	print(course)
#     	tree.create_node(course,course,parent="papa")
#     	# star+="*"
#     	# print(star)
#     	# time.sleep(2)
#     	pre_reqs = get_prerequisites(course)
#     	time.sleep(2)
#     	for pre in pre_reqs:
#             if(tree.get_node(pre) == None):
#                 tree.create_node(pre,pre,parent=course)
# for course in arr:
#     num = comparator(course)
#     # print(num)
#     if(num[0] == '2'):
#     	# print("We are jhere")
#     	print(course)
#     	tree.create_node(course,course,parent="papa")
#     	# star+="*"
#     	# print(star)
#     	# time.sleep(2)
#     	pre_reqs = get_prerequisites(course)
#     	time.sleep(2)
#     	for pre in pre_reqs:
#             if(tree.get_node(pre) == None):
#                 tree.create_node(pre,pre,parent=course)

# for course in arr:
#     num = comparator(course)
#     # print(num)
#     if(num[0] == '1'):
#     	print(course)
#     	# print("We are jhere")
#     	tree.create_node(course,course,parent="papa")
#     	# star+="*"
#     	# print(star)
#     	# time.sleep(2)
#     	pre_reqs = get_prerequisites(course)
#     	time.sleep(2)
#     	for pre in pre_reqs:
#             if(tree.get_node(pre) == None):
#                 tree.create_node(pre,pre,parent=course)

tree = create_tree(arr)
tree.show()
# print(tree.to_json())
tree.save2file('tree.txt')
  