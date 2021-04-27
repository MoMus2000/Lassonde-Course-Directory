from bs4 import BeautifulSoup
import requests
import os
import re
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


regex_with_no_spaces = '[A-Z]{2}\/[A-Z]{4} [0-9]{4} [0-9].00'
regex_with_spaces = '[A-Z]{2}\/ [A-Z]{4} [0-9]{4} [0-9].00'



def selenium_options():
	option = Options()
	option.add_argument("--disable-infobars")
	option.add_argument("start-maximized")
	option.add_argument("--disable-extensions")
	option.add_argument("--headless")
	option.add_argument("--log-level=OFF")
	return option

mapping = {'ACTG': '0', 'ADLW': '1', 'ADMS': '2', 'ALDR': '3', 'ANTH': '4', 'ARB': '5', 'ARTH': '6', 'ARTM': '7', 'ASL': '8', 'AUCO': '9', 'BBED': '10', 'BC': '11', 'BCHM': '12', 'BFSL': '13', 'BIOL': '14', 'BLIS': '15', 'BPHS': '16', 'BSUS': '17', 'BUEC': '18', 'BUSI': '19', 'CCLW': '20', 'CCY': '21', 'CDIS': '22', 'CDNS': '23', 'CH': '24', 'CHEM': '25', 'CIVL': '26', 'CLST': '27', 'CLTC': '28', 'CLTR': '29', 'CLWP': '30', 'CMCT': '31', 'COGS': '32', 'COMN': '33', 'COMS': '34', 'COOP': '35', 'COST': '36', 'CRIM': '37', 'CSLA': '38', 'DANC': '39', 'DATT': '40', 'DCAD': '41', 'DEMS': '42', 'DESN': '43', 'DEST': '44', 'DIGM': '45', 'DLLL': '46', 'DMGM': '47', 'DRAA': '48', 'DRST': '49', 'DVST': '50', 'ECON': '51', 'EDFE': '52', 'EDFR': '53', 'EDIN': '54', 'EDIS': '55', 'EDJI': '56', 'EDPJ': '57', 'EDPR': '58', 'EDST': '59', 'EDUC': '60', 'EECS': '61', 'EIL': '62', 'EMBA': '63', 'EN': '64', 'ENG': '65', 'ENSL': '66', 'ENTR': '67', 'ENVB': '68', 'ENVS': '69', 'ESL': '70', 'ESS': '71', 'ESSE': '72', 'EXCH': '73', 'FACC': '74', 'FACS': '75', 'FAST': '76', 'FILM': '77', 'FINE': '78', 'FND': '79', 'FNEN': '80', 'FNMI': '81', 'FNSV': '82', 'FR': '83', 'FRAN': '84', 'FREN': '85', 'FSL': '86', 'GCIN': '87', 'GEOG': '88', 'GER': '89', 'GFWS': '90', 'GK': '91', 'GKM': '92', 'GNRL': '93', 'GWST': '94', 'HEB': '95', 'HIMP': '96', 'HIST': '97', 'HLST': '98', 'HLTH': '99', 'HND': '100', 'HREQ': '101', 'HRM': '102', 'HUMA': '103', 'IBUS': '104', 'IHST': '105', 'ILST': '106', 'IMBA': '107', 'INDG': '108', 'INDS': '109', 'INDV': '110', 'INST': '111', 'INTE': '112', 'INTL': '113', 'ISCI': '114', 'IT': '115', 'ITEC': '116', 'JC': '117', 'JP': '118', 'JUDS': '119', 'KAHS': '120', 'KINE': '121', 'KOR': '122', 'LA': '123', 'LAL': '124', 'LASO': '125', 'LAW': '126', 'LAWB': '127', 'LAWH': '128', 'LAWL': '129', 'LIN': '130', 'LING': '131', 'LLDV': '132', 'LLS': '133', 'LREL': '134', 'LYON': '135', 'MACC': '136', 'MATH': '137', 'MBAN': '138', 'MDES': '139', 'MECH': '140', 'MFIN': '141', 'MGMT': '142', 'MINE': '143', 'MIST': '144', 'MKTG': '145', 'MMAI': '146', 'MODR': '147', 'MSTM': '148', 'MUSI': '149', 'NATS': '150', 'NRSC': '151', 'NURS': '152', 'OMIS': '153', 'ORCO': '154', 'ORGS': '155', 'OVGS': '156', 'PACC': '157', 'PANF': '158', 'PCS': '159', 'PERS': '160', 'PHED': '161', 'PHIL': '162', 'PHYS': '163', 'PIA': '164', 'PKIN': '165', 'PLCY': '166', 'POLS': '167', 'POR': '168', 'PPAL': '169', 'PPAS': '170', 'PROP': '171', 'PRWR': '172', 'PSYC': '173', 'PUBL': '174', 'RELS': '175', 'SCIE': '176', 'SELA': '177', 'SENE': '178', 'SGMT': '179', 'SLGS': '180', 'SLST': '181', 'SOCI': '182', 'SOCM': '183', 'SOSC': '184', 'SOWK': '185', 'SP': '186', 'SPTH': '187', 'STS': '188', 'SWAH': '189', 'SXST': '190', 'TECH': '191', 'TECL': '192', 'TESL': '193', 'THEA': '194', 'THST': '195', 'TLSE': '196', 'TRAN': '197', 'TRAS': '198', 'TXLW': '199', 'VISA': '200', 'WKLS': '201', 'WMST': '202', 'WRIT': '203', 'YSDN': '204'}

def get_course_list(options):
	print("Getting data..")
	driver = webdriver.Chrome(ChromeDriverManager().install(), options = options)
	url = 'https://w2prod.sis.yorku.ca/Apps/WebObjects/cdm.woa'
	driver.get(url)
	print("loading..")
	time.sleep(2)
	print("Done..")
	subject = driver.find_element_by_xpath("/html/body/p/table/tbody/tr[2]/td[2]/table/tbody/tr[2]/td/table/tbody/tr/td/ul/li[1]/ul/li[1]/a")
	subject.click()
	print("loading..")
	time.sleep(2)
	print("Done..")
	while(True):
		subs = input("Enter Subject CODE: ")
		if(subs.strip() == "back"):
			break
		option = mapping[subs.strip()]
		accounting = driver.find_element_by_xpath(f"//*[@id='subjectSelect']/option[{int(option)+1}]").click()
		button = driver.find_element_by_xpath("/html/body/table/tbody/tr[2]/td[2]/table/tbody/tr[2]/td/table/tbody/tr/td/form/table/tbody/tr[3]/td[2]/input").click()
		soup = BeautifulSoup(driver.page_source,'html.parser')

		whites = soup.find_all('tr',attrs={"bgcolor":"#ffffff"})
		blacks = soup.find_all('tr',attrs={"bgcolor":"#e6e6e6"})

		for whi in whites:
			index = whi.text.index("Fall/Winter")
			print(whi.text[0:index])

		for bla in blacks:
			index = bla.text.index("Fall/Winter")
			print(bla.text[0:index])

		driver.back()



def cant_think_of_a_name(input_str = ""):
	if(input_str == ""):
		input_str = input("Faculty Subject CourseNumber CourseCredit AccademicYear Term \nEg->(LE EECS 2031 3 2020 FW)\n")
	if(input_str.strip() == "back"):
		return None
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
	return soup


def parser(soup):
	try:
		heading = soup.find_all('p',{"class":"heading"})
		course_description_title = soup.find_all('strong')
		course_description = soup.find_all('p')
		print(heading[0].text)
		pre_req = course_description[3].text.find("Prerequisite")
		# print(pre_req)
		print(course_description_title[0].text)
		print(course_description[3].text[0:pre_req])
	except Exception as e:
		print("Info might not exist or something seems wrong...")


def subject_info():
	while(True):
		print("----------------------------------------------------------------------------")
		
		soup = cant_think_of_a_name()
		if(soup == None):
			break

		heading = soup.find_all('p',{"class":"heading"})
		# print(heading)
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
			while(True):
				subject_name = " ".join(heading[0].text.split())
				inp = input(f"Would you like to check out the PreReqs of {subject_name}\ny/n ?")
				if(inp == 'y' or inp == 'Y'):
					i = 0
					course_map = {}
					for course in pre_req_list2:
						course = course.replace("/"," ")
						print(str(i)+". "+course)
						course_map[i] = course+" 2020 FW"
						i+=1
					# print(course_map)
					choice = int(input("Which one ?"))
					s = cant_think_of_a_name(course_map[choice])
					parser(s)
				else:
					break
				#Call function again on the inputs after preparing them for execution
				#Strip down the ugly code and pls make it cleaner
			else:
				pass
				#Return back to the execution
def main():
	while(True):
		opt = input("Enter 1 for course list & 2 for course info: ")
		if(opt == "1"):
			options = selenium_options()
			get_course_list(options)
		else:
			subject_info()

main()


