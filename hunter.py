import requests
from bs4 import BeautifulSoup
import json
import smtplib

fromaddr = 'vakcinu.medziotojas@gmail.com'
toaddrs  = 'someone@gmail.com'
password = ''
URL = 'https://vilnius-vac.myhybridlab.com/selfregister/vaccine'

page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find('vaccine-rooms')

js1 = str(results).split(":vaccine-rooms='[")
js2 = js1[1].split("]'")
js3 = '{ "vacs" : ['+js2[0]+'] }'

parsed = json.loads(js3)
msg = ''

for i in parsed['vacs']:
	if i['free_total'] > 1 and i['name'] == "Vaxzevria (AstraZeneca)":
		msg = msg+'Atsirado '+i['name']+' '+str(i['free_total'])+' vakcinu!\n'
		
print(msg)
if msg > '':
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.ehlo()
	server.starttls()
	server.login(fromaddr,password)
	server.sendmail(fromaddr, toaddrs, msg)
	server.quit()

