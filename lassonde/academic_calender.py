from bs4 import BeautifulSoup
import requests


program = input("Year Faculty Program\n")
splits = program.split(" ")
year = int(splits[0])
Faculty = splits[1]
Major = splits[2]
year_before = year-1
if(year == 21):
	york_url = f'https://calendars.students.yorku.ca/2021-2022/programs/LE/computer-science'
elif(year == 20):
	york_url = f'https://2019-2020.calendars.students.yorku.ca/programs/{Faculty}{Major}'
else:
	york_url = f'https://previous-calendars.students.yorku.ca/{year_before}-{year}/programs/{Faculty}{Major}'

req = requests.get(york_url)
# print(req.text)
soup = BeautifulSoup(req.text,'html.parser')
print(soup.find('a'))