#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Check for all required python dependencies first

try:	
	import sys
	import argparse
	import subprocess
	import shlex
except ImportError, e:
	python_install = raw_input("\nMissing required python dependencies: sys argparse subprocess shlex. Install them now? [y/n]")
	if python_install == 'y' or python_install == 'yes':
		install_process = subprocess.Popen(['pip install sys argparse subprocess shlex'], stdout=subprocess.PIPE, shell=True)
		(out, err) = install_process.communicate()
		print(out);
	else:
		print('Error: unmet dependencies, leaving...')
		sys.exit(0)

# Check for system specific dependencies

nslookup = subprocess.Popen(['command -v nslookup'], stdout=subprocess.PIPE, shell=True)
(out, err) = nslookup.communicate()	

if len(out) == 0:
	nslookup_install = raw_input("\n'dnsutils' package is a required dependency but it is not installed in your system. Install now? [y/n]")
	if nslookup_install == 'y' or nslookup_install == 'yes':
		install_process = subprocess.Popen(['sudo apt-get install -y dnsutils'], stdout=subprocess.PIPE, shell=True)
		(out, err) = install_process.communicate()
		print(out);
	else:
		print('Error: unmet dependency, leaving...')
		sys.exit(0)


print('\n---------------- MIXFLARE v0.12 ----------------\n')

#Create options for single string input or list of strings

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', action="store_true", dest='input', help='Simple Lookup. Searches for availability of the specified domain name. (.com and .net top-level domains supported)')
parser.add_argument('-l', '--list-domains', action="store_true", dest='list', help='Advanced search. This option takes in a list of space separated strings, generates all possible (and best) combinations between them, and then checks their avalability as domain names via DNS lookup.')
parser.add_argument('-c', '--com', action="store_true", dest='com_domains', help='Filter results by .com domains only.')
parser.add_argument('-n', '--net', action="store_true", dest='net_domains', help='Filter results by .net domains only.')
parser.add_argument('--version', action='version', version='Mixflare v0.12')

args = parser.parse_args()

# If not -c or -n option, don't even bother

if not args.com_domains and not args.net_domains and not args.list:	
	print('Please specify a TLD option: -c for .com, -n for .net domains or both. e.g.: domain-finder -c')
	sys.exit(0)


############### main functions ###############

def perform_simple_lookup():
	
	try:
		args.input = raw_input('\nPlease enter a single word to search for (i.e: with no TLS extension): \n')
		
		# sanitize input string
		invalid = set(';&(){}!¡?¿=.,_$@^*¨%"<>') 
		
		if any((c in invalid) for c in args.input):
			print("Error: ';&(){}!¡?¿=.,_$@^*¨%\"<>' characters not permitted")
			sys.exit(0)
		else:
			domInput = args.input

	except ValueError:
		print("Wrong input type. Please try again.")
	
	except KeyboardInterrupt:
		print "\nUser interrupted. Bye!"
        	sys.exit()

	available = []

	if args.com_domains:
		xcom = domInput + ".com"
		response_com = subprocess.Popen(["nslookup " + xcom], stdout=subprocess.PIPE, shell=True)
		(out, err) = response_com.communicate()	
		if "NXDOMAIN" in out:
			available.append(xcom)

		
	if args.net_domains:
		xnet = domInput + ".net"
		response_net = subprocess.Popen(["nslookup " + xnet], stdout=subprocess.PIPE, shell=True)
		(out, err) = response_net.communicate()
		if "NXDOMAIN" in out:
			available.append(xnet)

	if len(available) < 1:
		print('\nSorry, there are no unregistered domain names matching your criteria.\nYou should try again with different words.')
		perform_simple_lookup() # Recursive call to prompt again.
	else:
		print('\n' + str(len(available)) + ' available domain(s):\n' + '\n'.join(available))


def perform_advanced_search():

	try:

		# Create new list from the words given.

		args.list = raw_input('\nPlease enter a list of space-separated words (5 max): \n')
	
		# sanitize input string
		invalid = set(';&(){}!¡?¿=.,_$@^*¨%"<>') 

		if any((c in invalid) for c in args.list):
			print("Error: ';&(){}!¡?¿=.,_$@^*¨%\"<>' characters not permitted")
			sys.exit(0)
		else:
			domList = args.list
			domList = shlex.split(domList)
	
		if len(domList) > 5:
			print('\n ----> Maximum of elements reached! Please enter 5 or less.')
			perform_advanced_search() # Recursive call to prompt again.
		
	except ValueError:
		print("Wrong input type. Please try again.")

	except KeyboardInterrupt:
		print "\nUser interrupted. Bye!"
        	sys.exit()

	# Generate all possible two-word combinations between the elements of the list.
	# Avoid combinations of same words. Total amount generated: (x^2 - x) where x = --list-domains
	
	combos = []

	for x in domList:
		for y in domList:

			if not x == y: 
				combos.append(x + y)
				
				
	combosLen = len(combos)
				
	# Check for available domains within the word list. Total amount of requests (x^2 - x)*2
	
	available = []

	for x in combos:

		if args.com_domains:
			xcom = x + ".com"
			response_com = subprocess.Popen(["nslookup " + xcom], stdout=subprocess.PIPE, shell=True)
			(out, err) = response_com.communicate()
			if "NXDOMAIN" in out:
				available.append(xcom)
		
		if args.net_domains:
			xnet = x + ".net"
			response_net = subprocess.Popen(["nslookup " + xnet], stdout=subprocess.PIPE, shell=True)
			(out, err) = response_net.communicate()
			if "NXDOMAIN" in out:
				available.append(xnet)
		
		# Display progress bar on tty
		xVal = combos.index(x) + 1
		percent = int(xVal/float(combosLen) * 100)
		lines = int(xVal/float(combosLen) * 30)

		sys.stdout.write('\r')
		sys.stdout.write("[%-30s] %d%%" % ('='* lines, percent))
		sys.stdout.flush()
		


	if len(available) < 1:
		print('\n\nSorry, there are no unregistered domain names matching your criteria.\nYou should try again with different words.')
		perform_advanced_search() # Recursive call to prompt again.
	else:
		print('\n\n' + str(len(available)) + ' available domain(s):\n' + '\n'.join(available))

############### /main functions ###############


if not args.list:
	
	# Always default to Simple Lookup.
    	perform_simple_lookup()
    
else:	
	perform_advanced_search()	
	

# EOF
