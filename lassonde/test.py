import requests
from bs4 import BeautifulSoup



# def print_subjects(faculty_code):
# 	mapping = {
# 	"LE":["CIVL","COOP","CSE","EATS","EECS","ENG","ESSE","MECH","TECL"],
# 	"LW":["LAW"],
# 	"SC":["BC","BCHM","BIOL","BPHS","CHEM","COOP","ENVB","GEOG","ISCI","MATH","NATS","NRSC","PHYS","RYER","SENE","STS"],
# 	"SB":["ACTG","ARTM","BSUS","DCAD","ECON","EMBA","ENTR","ETHC","EXCH","FINE","FNEN","FNSV","HIMP","IBUS","IMBA","INTL","MACC","MBAN","MFIN","MGMT","MINE","MKTG","MMAI","MSBA","MSTM","NMLP","OMIS","ORGS","PLCY","PROP","PUBL","SGMT","SOCM"]}

# 	return mapping.get(faculty_code)

# def print_faculties():
# 	york_faculties_url = "https://w2prod.sis.yorku.ca/Apps/WebObjects/cdm.woa/fa=LE&sj=EECS"
# 	req = requests.get(york_faculties_url)
# 	soup = BeautifulSoup(req.text,'html.parser')
# 	tags = soup.find_all('a')
# 	link = ''
# 	for a in tags:
# 		if(a.text == 'Subject'):
# 			link = 'https://w2prod.sis.yorku.ca'+a['href']
# 	if(link != ''):
# 		# print(link)
# 		soup = BeautifulSoup(requests.get(link).text,'html.parser')
# 		facs = soup.find_all('select',attrs={"id":"subjectSelect"})
# 		fx = ''
# 		for fac in facs:
# 			fx = fx+fac.text		
# 		fx =fx.split("-")
# 		for f in fx:
# 			print(f[0:-1])

# def print_faculties_part2():
# 	return"""
# 	(AK)Atkinson Faculty of Liberal & Professional Studies
#         (AP)Faculty of Liberal Arts and Professional Studies
#   	(AS)Faculty of Arts
#  	(ED)Faculty of Education
#  	(ES)Faculty of Environmental Studies
#  	(EU)Faculty of Environmental and Urban Change	
#  	(FA)School of the Arts, Media, Performance and Design	
#  	(GL)Collège universitaire Glendon	
#  	(GS)Faculty of Graduate Studies	
#  	(HH)Faculty of Health	
#  	(LE)Lassonde School of Engineering*	
#  	(LW)Osgoode Hall Law School*	
#  	(SB)Schulich School of Business
#  	(SC)Faculty of Science*
#  	"""



# print_faculties()
# print(print_faculties_part2())
# print("\n")
# print(print_subjects("SB"))


import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

option = Options()
option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")
option.add_argument("--headless")
# option.add_experimental_option('excludeSwitches',['enable-logging']);

driver = webdriver.Chrome(ChromeDriverManager().install(), options = option)
url = 'https://w2prod.sis.yorku.ca/Apps/WebObjects/cdm.woa'
driver.get(url)
time.sleep(2)


mapping = {'ACTG': '0', 'ADLW': '1', 'ADMS': '2', 'ALDR': '3', 'ANTH': '4', 'ARB': '5', 'ARTH': '6', 'ARTM': '7', 'ASL': '8', 'AUCO': '9', 'BBED': '10', 'BC': '11', 'BCHM': '12', 'BFSL': '13', 'BIOL': '14', 'BLIS': '15', 'BPHS': '16', 'BSUS': '17', 'BUEC': '18', 'BUSI': '19', 'CCLW': '20', 'CCY': '21', 'CDIS': '22', 'CDNS': '23', 'CH': '24', 'CHEM': '25', 'CIVL': '26', 'CLST': '27', 'CLTC': '28', 'CLTR': '29', 'CLWP': '30', 'CMCT': '31', 'COGS': '32', 'COMN': '33', 'COMS': '34', 'COOP': '35', 'COST': '36', 'CRIM': '37', 'CSLA': '38', 'DANC': '39', 'DATT': '40', 'DCAD': '41', 'DEMS': '42', 'DESN': '43', 'DEST': '44', 'DIGM': '45', 'DLLL': '46', 'DMGM': '47', 'DRAA': '48', 'DRST': '49', 'DVST': '50', 'ECON': '51', 'EDFE': '52', 'EDFR': '53', 'EDIN': '54', 'EDIS': '55', 'EDJI': '56', 'EDPJ': '57', 'EDPR': '58', 'EDST': '59', 'EDUC': '60', 'EECS': '61', 'EIL': '62', 'EMBA': '63', 'EN': '64', 'ENG': '65', 'ENSL': '66', 'ENTR': '67', 'ENVB': '68', 'ENVS': '69', 'ESL': '70', 'ESS': '71', 'ESSE': '72', 'EXCH': '73', 'FACC': '74', 'FACS': '75', 'FAST': '76', 'FILM': '77', 'FINE': '78', 'FND': '79', 'FNEN': '80', 'FNMI': '81', 'FNSV': '82', 'FR': '83', 'FRAN': '84', 'FREN': '85', 'FSL': '86', 'GCIN': '87', 'GEOG': '88', 'GER': '89', 'GFWS': '90', 'GK': '91', 'GKM': '92', 'GNRL': '93', 'GWST': '94', 'HEB': '95', 'HIMP': '96', 'HIST': '97', 'HLST': '98', 'HLTH': '99', 'HND': '100', 'HREQ': '101', 'HRM': '102', 'HUMA': '103', 'IBUS': '104', 'IHST': '105', 'ILST': '106', 'IMBA': '107', 'INDG': '108', 'INDS': '109', 'INDV': '110', 'INST': '111', 'INTE': '112', 'INTL': '113', 'ISCI': '114', 'IT': '115', 'ITEC': '116', 'JC': '117', 'JP': '118', 'JUDS': '119', 'KAHS': '120', 'KINE': '121', 'KOR': '122', 'LA': '123', 'LAL': '124', 'LASO': '125', 'LAW': '126', 'LAWB': '127', 'LAWH': '128', 'LAWL': '129', 'LIN': '130', 'LING': '131', 'LLDV': '132', 'LLS': '133', 'LREL': '134', 'LYON': '135', 'MACC': '136', 'MATH': '137', 'MBAN': '138', 'MDES': '139', 'MECH': '140', 'MFIN': '141', 'MGMT': '142', 'MINE': '143', 'MIST': '144', 'MKTG': '145', 'MMAI': '146', 'MODR': '147', 'MSTM': '148', 'MUSI': '149', 'NATS': '150', 'NRSC': '151', 'NURS': '152', 'OMIS': '153', 'ORCO': '154', 'ORGS': '155', 'OVGS': '156', 'PACC': '157', 'PANF': '158', 'PCS': '159', 'PERS': '160', 'PHED': '161', 'PHIL': '162', 'PHYS': '163', 'PIA': '164', 'PKIN': '165', 'PLCY': '166', 'POLS': '167', 'POR': '168', 'PPAL': '169', 'PPAS': '170', 'PROP': '171', 'PRWR': '172', 'PSYC': '173', 'PUBL': '174', 'RELS': '175', 'SCIE': '176', 'SELA': '177', 'SENE': '178', 'SGMT': '179', 'SLGS': '180', 'SLST': '181', 'SOCI': '182', 'SOCM': '183', 'SOSC': '184', 'SOWK': '185', 'SP': '186', 'SPTH': '187', 'STS': '188', 'SWAH': '189', 'SXST': '190', 'TECH': '191', 'TECL': '192', 'TESL': '193', 'THEA': '194', 'THST': '195', 'TLSE': '196', 'TRAN': '197', 'TRAS': '198', 'TXLW': '199', 'VISA': '200', 'WKLS': '201', 'WMST': '202', 'WRIT': '203', 'YSDN': '204'}
# print(mapping)

subject = driver.find_element_by_xpath("/html/body/p/table/tbody/tr[2]/td[2]/table/tbody/tr[2]/td/table/tbody/tr/td/ul/li[1]/ul/li[1]/a")
subject.click()
time.sleep(2)
while(True):
	subs = input("Enter Subject CODE: ")
	option = mapping[subs]
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
