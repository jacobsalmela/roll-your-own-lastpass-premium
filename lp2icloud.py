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
			password = row[2]
			fixed_password = escape_password(password)
			print fixed_password
			url = row[0]
			server = row[4]
			osascript('''
			tell application "Safari" to close every window
			tell application "Safari"
				activate
				open location "%(url)s"
				repeat
					if (do JavaScript "document.readyState" in document 1) is "complete"
						exit repeat
					else 
						false
					end if
				end repeat
			end tell
			delay 5.0
			
			tell application "System Events"
			tell process "Safari"
				set textFields to window 1
				set allUIElements to entire contents of textFields
				
				repeat with anElement in allUIElements
					try
						if role description of anElement is "text field" then
							set value of anElement to "%(username)s"
						else if role description of anElement is "secure text field" then
							set value of anElement to "%(fixed_password)s"
							set focus to anElement
						end if
					end try
				end repeat
			end tell
			end tell
			tell application "Safari" to activate
			tell application "System Events"
				keystroke return

				delay 2.0
			end tell

			tell application "System Events"
				tell process "Safari"
				try
					click button "Save Password" of sheet 1 of window 1
				end try
				end tell
			say "Password saved" using "Samantha"
			end tell

			''' % locals())