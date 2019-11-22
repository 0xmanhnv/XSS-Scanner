try:
	import requests
	from bs4 import BeautifulSoup
	import os
	import sys
	from colorama import Fore, Style
except Exception as e:
	print(e)

os.system("clear")


file = input(Fore.CYAN + Style.BRIGHT + ">> [?] Enter List With XSS Payloads: ")
payloads = open(file, "r")
read_lines = payloads.readlines()

host = input(Fore.CYAN + Style.BRIGHT + ">> [?] Enter Target Url: ")
inputs = []

print(Fore.CYAN + Style.BRIGHT + ">> [*] Searching WebPage For Inputs")
r = requests.get(host)
content = r.text
soup = BeautifulSoup(content, "html5lib")
inputss = soup.find_all("input")
for input in inputss:
	try:
		inputs.append(input['name'])
		pass
	except KeyError:
		pass

if(len(inputs) == 0):
	print(Fore.RED + Style.BRIGHT + ">> [!] No Inputs Have Been Found. Try Again With Another Webpage")
	sys.exit()
else:
	print(Fore.GREEN + Style.BRIGHT + ">> [+] Amout Of Inputs Found: " + str(len(inputs)))



def scan_xss():
	for input in inputs:
		for payload in read_lines:
			vuln_url = requests.get(host + "/?" + str(input) + "=" + str(payload))
			print(Fore.CYAN + Style.BRIGHT + ">> [*] Testing Parameter: " +  str(input) + " With Following XSS Payload: " + str(payload))
			if(payload in vuln_url.text):
				print(Fore.GREEN + Style.BRIGHT + ">> [+] Parameter: " + str(input) + " Is Not Sanitized Properly And Vulnerable To XSS Attacks")
				print(Fore.GREEN + Style.BRIGHT + "+"*90)
			else:
				print(Fore.RED + Style.BRIGHT + ">> [+] Parameter: " + str(input) + " Is Sanitized Properly And Not Vulnerable To XSS Attacks")
				print(Fore.RED + Style.BRIGHT + "-"*90)
scan_xss()
