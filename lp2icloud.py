#!/usr/bin/python
#---------IMPORTS-----------
import csv
from subprocess import call
from os import system

#--------VARIABLES----------
# Put the path to your CSV file in the quotes below, leave the "rb" alone
cr = csv.reader(open("~/Downloads/exported_passwords.csv","rb"))

#---------SCRIPT------------
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
			url = row[0]
			server = row[4]
			print str(idx) + "     **ADDING: " + server
			lp2icloud = """
osascript -e '--close any open windows so the page is always "window 1," which is used in the steps below to set the username and password
tell application "Safari" to close every window
tell application "Safari"
	activate
	--open location "https://jamfnation.jamfsoftware.com/login.html"
	open location "'%(url)s'"
	repeat
		--wait for the page to be loaded before doing anything
		if (do JavaScript "document.readyState" in document 1) is "complete" then exit repeat
		delay 1 -- wait a second before checking again
	end repeat
end tell
--wait for page to load
delay 5.0
tell application "System Events"
	tell process "Safari"
		activate
		--variable to hold HTML content
		set textFields to UI element 1 of scroll area 1 of group 1 of group 1 of group 4 of window 1
		--another variable to hold each scriptable-element
		set allUIElements to entire contents of textFields
		
		--for each element, check if it is a username or password field and fill in the appropriate data
		repeat with anElement in allUIElements
			try
				if role description of anElement is "text field" then
					set value of anElement to "'%(username)s'"
				else if role description of anElement is "secure text field" then
					set value of anElement to "'%(password)s'"
					set focus to anElement
					exit repeat
				end if
			end try
		end repeat
	end tell
end tell
--make sure Safari is active before pressing enter to log in
tell application "Safari" to activate
tell application "System Events"
	keystroke return
	--give the "Save Password" sheet a moment to appear
	delay 2.0
end tell
tell application "System Events"
	tell process "Safari"
		try
			--Save the password to Safari/iCloud keychain
			click button "Save Password" of sheet 1 of window 1
		end try
	end tell
	say "Password saved for "'%(password)s'"" using "Samantha"
end tell
'
""" 
			# Execute Applescript code using Python variables.
			system(lp2icloud % locals())
