#!/usr/bin/python
#---------IMPORTS-----------
import csv
from subprocess import call

#--------VARIABLES----------
# Put the path to your CSV file in the quotes below, leave the "rb" alone
cr = csv.reader(open("/Users/jacob_salmela/schedule.csv","rb"))
kind = "Web form password" # Application password
type = "form"
auth_type = "form"
protocol = "htps"

#---------SCRIPT------------
for idx,row in enumerate(cr):
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
			url = row[0]
			#server = row[4] + " (" + username + ")"
			server = row[4]
			
			#print server
			# Use the bash security command to:
			# 		Add an Internet password, with the kin(-d), p(-r)otocol, authentication (-t)ype, (-A)llow all apps to access, (-U)pdate if existing, comment (-j), (-s)erver, (-a)ccount, and pass(-w)ord
			#call(["/usr/bin/security", "add-internet-password", "-D", "Web form password", "-r", "http", "-t", "dflt", "-U", "-j", "default", "-s", server, "-a", username, "-w", password])
			# "Works" for non-https sites
			call(["/usr/bin/security", "add-internet-password", 
					# REQUIRED: Account
					"-a", username,
					# REQUIRED: Server
					"-s", server, 
					# REQUIRED: Password
					"-w", password,
					# Creator   
					#"-c", creator, 
					# Type
					#"-C", type, 
					# Kind of password
					"-D", kind,
					# Comment
					#"-j", commment, 
					# Label
					#"-l", label,
					# Path
					#"-p", path, 
					# Port number 
					#"-P", port, 
					# Protocol
					"-r", protocol,
					# Authentication type
					#	http BASIC
					#	httd DIGEST
					#	form FORM
					#	dflt DEFAULT
					#	0	 ANY
					"-t", auth_type, 
					# Any app can access
					"-A", 
					# This app can access 
					#"-T", app 
					# Update if already existing
					"-U"])

			print str(idx) + "     **ADDED: " + url
			print "     **USING" + kind + type + auth_type + protocol