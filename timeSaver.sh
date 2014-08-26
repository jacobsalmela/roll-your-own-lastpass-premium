#!/bin/bash
# Change 60 to however many passwords you have to authenticate for
for f in {1..60}
do
sleep 1
# Enter your password below
osascript -e <<EOF 'tell application "System Events"
	tell process "SecurityAgent"
	set value of text field 1 of window 1 to "password"
	end tell
	tell application "system events" to keystroke return
	end tell'
EOF
done