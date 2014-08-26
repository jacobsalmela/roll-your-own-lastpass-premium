#!/usr/bin/python
#---------IMPORTS-----------
import csv
from subprocess import call

#--------VARIABLES----------
# Put the path to your CSV file in the quotes below, leave the "rb" alone
cr = csv.reader(open("/Users/jacob_salmela/schedule.csv","rb"))

#---------SCRIPT------------
for row in cr:
	# If it is a Secure Note, do nothing, as we only want usernames and passwords for Websites
	if row[0] == "http://sn":
		pass
	else:
		#['url', 'username', 'password', 'extra', 'name', 'grouping', 'fav']
		# Don't save the column names as a keychain entry
		if row[1] == "username":
			pass
		elif row[2] == "password":
			pass		
		elif row[4] == "name":
			pass
		else:
			username = row[1]
			password = row[2]
			# Prefix site names with LP so we know they were imported from LastPass
			# This makes it easier to drag them into the iCloud section of Keychain Access
			server = "LP-" + row[4]
			# Use the bash security command to:
			# 		Add an Internet password, with the (-s)erver, (-a)ccount, and pass(-w)ord
			call(["/usr/bin/security", "add-internet-password", "-s", server, "-a", username, "-w", password])
			print "**ADDED: " + server
