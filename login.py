#!/usr/bin/env python3
import os
import sys

# Local imports
import core

notesDir = os.environ['HOME'] + '/.pluralnotes' # Used to define the main notes directory and/or work with it.

# Login sequence; tries to account for upper/lowercase and exits if the user requests it, else loops prompt until a valid login is entered. Allows users to create nonexistent username directories as long as they don't violate these restrictions, or log into an existing one.
# TODO: Check if a username including a backslash is a problem at all.
# TODO: Figure out password authentication and directory encryption so inter-username privacy is possible. This is meant to be a multiuser notekeeping utility on one shared computer account, so passwords are kind of important for that. Also MAKE SURE that the passwords are stored encrypted, and encrypt the entered password with the same hash to compare. People reuse passwords a lot and it's a security hazard to store them in plaintext. Make sure the password is not displayed as it's typed, too.
def login():
	global username
	while 1:
		username = input(" Enter your name (case-sensitive), or q to exit: ")
		# If user does not yet exist:
		# Deal with whitespaces and empty strings
		if os.path.isdir(notesDir + "/" + username) == False:
			if username.isspace() == True or " " in username or "\n" in username or "\t" in username:
				core.clear()
				print(" Usernames cannot contain spaces, tabs, or new lines. Please enter a valid username.")
			elif username == False or username == "":
				core.clear()
				print(" Please enter a valid username.")

			# Disallow reserved shared directory name to avoid naming conflict
			elif username == "sharednotes" or username == "archives":
				core.clear()
				print(" Name reserved for shared notes or archives. Please enter a valid username.")

			# Give the user a way to exit the program from this prompt so they're not stuck looping endlessly until they make a user
			elif username.lower() == "q":
				core.clear()
				print("See you next time!")
				sys.exit(0)

			# Ask if the person wants to create user if it doesn't already exist, and create them if yes
			else:
				print(" This user does not exist. Would you like to create a user called " + username + "?")
				userCheck = input(" Input <y/n>: ").lower()
				if userCheck == "y" or userCheck == "yes":
					# os.mkdir(username)
					core.dirChanger(username)
					if os.path.isdir("data") == False: os.mkdir("data")
					os.chdir(notesDir)
					print (" " + username + " created. You may now log in!")

		# Log in valid existing users and proceed to the actual program
		# TODO: Add password authentication and decryption of logged-in user.
		elif os.path.isdir(notesDir + "/" + username) == True:
			userDir = notesDir + "/" + username
			if os.path.isfile(userDir + "/data/settings.txt") == False:
				if os.name == "nt":
					defaultEditor = os.environ.get('EDITOR') if os.environ.get('EDITOR') else 'notepad'
				else:
					defaultEditor = os.environ.get('EDITOR') if os.environ.get('EDITOR') else 'nano'
				f = open(notesDir + "/" + username + "/data/settings.txt", "a")
				f.write(defaultEditor + "\n")
				f.write("10" + "\n")
				f.write("True" + "\n")
				f.write("False" + "\n")
				f.write("-" + "\n")
				f.write("Warning: Do not edit spacing!" + "\n")
				f.write("If manually editing settings, True/False must be capitalized. If you mess it up, don't worry- you can either delete this file (the program will remake it) or reset to the default in settings.")
				f.write("""Settings in order:
				Editor
				Page size
				Include date in new note names
				Include username in new note names""")
			break

		# Deal with edge cases and weird inputs, because you just know that someone is going to break this in an unexpected way.
		else: print(" Please enter a valid username.")
