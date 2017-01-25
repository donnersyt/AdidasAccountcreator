# ADIDAS Account Creator v0.1
# Made by Donners
# https://github.com/donnersyt/AdidasAccountCreator

### Dependencies 
# Requests
# BS4
acceptedRegions = ["GB","US"]

print("\n" * 20)
version = "v0.1"
print(version + str(" Adidas Account Creator"))
from datetime import datetime
import requests
import configparser
import random
try:
	import bs4
except:
	import BeautifulSoup
import json
import os
if "nt" in os.name:
	windows = True
else:
	windows = False
def log(event):
	print(str(datetime.now().strftime("%H:%M:%S")) + str(" -- " + str(event)))



config = configparser.ConfigParser()
if windows:
	file = os.path.	isfile("/config.cfg")
	path = "/config.cfg"
elif not windows:
	file = os.path.isfile("./config.cfg")
	path = "./config.cfg"
if not file:
	log("config.cfg not found!")
elif file:
	config.read(path)
	region = config.get("setup", 'region').upper()
	sleep = config.get("setup", "sleep")
	if region not in acceptedRegions:
		log("Region " +str(region) + " is not currently supported :(")
		exit()
	print("Region = " +str(region))


def setUrl():
	if region == "GB":
		domain = "co.uk"
		lang = "en_GB"
	elif region == "US":
		domain = "com"
		lang = "en_US"
	CSRFurl = "https://www.adidas.{}/on/demandware.store/Sites-adidas-{}-Site/{}/MyAccount-Register".format(domain, region, lang)
	POSTurl = "https://cp.adidas.{}/web/eCom/{}/accountcreate".format(domain, lang)
	return CSRFurl, POSTurl

def runCreation():
	headers = {
	"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"
	}
	print(url[0])
	a = requests.get(url[0], headers = headers)		# Issue here with it not loading JS so it does not fetch the CSRFToken
	soup = bs4.BeautifulSoup(a.text, "html.parser")
	#soup = soup.find("body").find("div",{"id":"main"})
	#soup = soup["value"]
	print(soup)
	for i in range(numberOfAccounts):
		session = requests.session()



if __name__ == "__main__":
	numberOfAccounts = 10
	"""
	numberOfAccounts = int(input("Please Enter the total number of accounts to make: "))
	if numberOfAccounts >= 200:
		log("You can not make more than 200 accounts as of now.")
	"""
	url = setUrl()
	runCreation()

