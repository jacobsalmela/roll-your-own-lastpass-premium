#!/usr/bin/python
#---------IMPORTS-----------
import csv
# Must run sudo pip install osascript
from osascript import osascript
from os import system

#--------VARIABLES----------
# Put the path to your CSV file in the quotes below, leave the "rb" alone
cr = csv.reader(open("~/Downloads/exported_passwords.csv","rb"))

#---------SCRIPT------------
##############################
def escape_password(password):
	escaped_password = ''
	for c in range(0, len(password)):
		# Escape characters that will cause syntax problems in the script
		if (password[c] == "\\"):
			escaped_password+="\\\\"
		elif (password[c] == '"'):
			escaped_password+="\\\""
		elif (password[c] == "'"):
			escaped_password+="\\\'"																	
		else:
			escaped_password+=str(password[c])
	return escaped_password


for idx,row in enumerate(cr):
	# If it is a Secure Note, do nothing, as we only want usernames and passwords for Websites
	if row[0] == "http://sn":
		pass
	else:
		# Don't save the column names as a keychain entry
		#['url', 'username', 'password', 'extra', 'name', 'grouping', 'fav']
		if row[1] == "username":
			pass
		elif row[2] == "password":
			pass		
		elif row[4] == "name":
			pass
		else:
			username = row[1]
			# "%(username)s"
			password = row[2]
			fixed_password = escape_password(password)
			# "%(fixed_password)s"
			url = row[0]
			# "%(url)s"
			server = row[4]
			print str(idx) + ":	" + server
			print username
			print password
			osascript('''
			on open_url(address)
			tell application "Safari"
				close every window
				activate
				open location address
			end tell
			end open_url



			on wait_for_page_to_load()
			delay 0.5
			tell application "Safari"
			repeat
				set thePage to source of document in window 1
				if thePage contains "</html>" then
					return true
					exit repeat
				else
					delay 0.5
				end if
			end repeat
			end tell
			end wait_for_page_to_load




			on fill_in_fields(username, passwd)
			tell application "System Events"
				tell process "Safari"
					repeat until not (exists window 1)
					set allUIElements to entire contents of window 1
					repeat with anElement in allUIElements
					try
						if role description of anElement is "text field" then
							set value of anElement to username
						else if role description of anElement is "secure text field" then
							set value of anElement to passwd
						end if
					end try
					end repeat
					
					try
						click button "Save Password" of sheet 1 of window 1
					end try
					end repeat
				end tell
			end tell
			end fill_in_fields
	
	
	
	
			open_url("%(url)s")
			wait_for_page_to_load()
			fill_in_fields("%(username)s", "%(fixed_password)s")

			''' % locals())