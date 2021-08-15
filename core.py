#!/usr/bin/env python3
import os
import sys
from datetime import date
from time import sleep
import re
from shutil import move
import platform

# Local imports
import login

if platform.system() == "Windows":
    envHome = os.getenv('APPDATA')
else:
    envHome = os.environ['HOME']

# Forgive me father, for this code is messy. At least it works.

# Set editor var via env, or default to nano on Linux and Mac, and Notepad on Windows if none is set.
if os.name == "nt":
	editor = os.environ.get('EDITOR') if os.environ.get('EDITOR') else 'notepad'
else:
	editor = os.environ.get('EDITOR') if os.environ.get('EDITOR') else 'nano'

sharedSelection = "0" # Must be 0, else you may accidentally call an if statement. Used in a while loop to determine user actions and sometimes as an exit condition. There's probably a way to define this later and save a few lines, but make that a TODO since basic functionality comes first.
todayDate = str(date.today()) # Used to append the date onto the end of files, and hide the date when casually viewing them.

def clear(): os.system('cls' if os.name == 'nt' else 'clear') # Function is called to clear the terminal. Makes it look pretty and easy to read instead of smacking someone with more than one visible menu.

# Changes working directory; creates the requested directory if it doesn't exist
def dirChanger(dirName):
	if os.path.isdir(dirName) == False: os.mkdir(dirName)
	os.chdir(dirName)
	workingDir = os.path.dirname

def paginateDir(dirName):
	feedback = ""
	username = login.username
	settingsFile = envHome + '/.pluralnotes' + "/" + username + "/data/settings.txt"
	settings = open(settingsFile, 'r').readlines()
	editor = str(settings[0]).strip()
	fileCount = int(str(settings[1]).strip())
	navigator = 0
	# Create a list of working directory contents. Sort the list alphabetically.
	dirContents = os.listdir()
	dirContents = sorted(dirContents, key=str.lower)
	dirContentsLength = len(dirContents)
	selection = 0 # Used by user for input, and to break loop on request
	bottomPageNumber = 0 # Lower limit of a page
	pageCount = 1 # Which page we're on. Needs to be separate from bottomPageNumber because that variable increments by the number in fileCount, and page number increments by one.
	topPageNumber = bottomPageNumber + fileCount # Upper limit of a page.
	if len(dirContents) == 0:
		while navigator != "q":
			print()
			print(" No notes here!")
			print()
			print("\x1b[31m" + " q: quit" + "\x1b[0m")
			if feedback != "":
				print()
			print("\x1b[33m" + " " + feedback + "\x1b[0m")
			navigator = input(" Enter selection: ").lower()
			if navigator == "q":
				clear()
				break
			else:
				clear()
				feedback = "Invalid input."
	else:
		holderList = []
		# Remove folders from directory list- there's bound to be a better way to do it but this works for now.
		for elem in dirContents:
			isFile = os.path.isfile(elem)
			if isFile == True:
				holderList.append(str(elem))
		dirContents = holderList
		dirContents = sorted(dirContents, key=str.lower)
		search = False
		outOfNotes = False
		while selection != "q":
			print()
			print(" Page " + str(pageCount))
			print()
			# Paginate directory. Sort of an odd way to do it, but it works and I couldn't get another method working. Still learning Python! Definitely an area to refactor later.
			for elem in dirContents[bottomPageNumber:topPageNumber]:
				print(str(" " + str(dirContents.index(elem))) + ". " + str(elem)) # Yes, the outermost string is needed. It throws a type error otherwise.
			print()
			print("\x1b[31m" + " n: next page" + "\x1b[0m")
			print("\x1b[33m" + " b: previous page" + "\x1b[0m")
			print("\x1b[32m" + " s: search for notes" + "\x1b[0m")
			if search == True:
				print("\x1b[36m" + " c: clear search" + "\x1b[0m")
			print("\x1b[34m" + " e: read/edit note" + "\x1b[0m")
			print("\x1b[35m" + " d: delete note" + "\x1b[0m")
			print("\x1b[31m" + " q: quit" + "\x1b[0m")
			if feedback != "":
				print()
			print("\x1b[33m" + " " + feedback + "\x1b[0m")
			# User input time!
			navigator = input(" Enter selection: ").lower()
			# Address running out of notes so the user can't iterate through empty pages
			if navigator == "n" and dirContentsLength < topPageNumber + pageCount:
				clear()
				feedback = "No more notes."
			elif navigator == "b" and pageCount == 1:
				clear()
				# Fixes weird change in size of list that happens otherwise by resetting to page "one" (0)
				bottomPageNumber = 0
				topPageNumber = bottomPageNumber + fileCount
				pageCount = 1
				feedback = "You're already on the first page!"
			# Regular navigation
			elif navigator == "n":
				clear()
				# Iterate to next page.
				bottomPageNumber = bottomPageNumber + fileCount
				topPageNumber = bottomPageNumber + fileCount
				pageCount = pageCount + 1
				feedback = ""
			elif navigator == "b" and pageCount != 1:
				clear()
				# Iterate to previous page.
				bottomPageNumber = bottomPageNumber - fileCount
				topPageNumber = bottomPageNumber + fileCount
				pageCount = pageCount - 1
				feedback = ""
			# Address trying to change pages when there are no notes
			elif navigator == "n" and len(dirContents[bottomPageNumber:topPageNumber]) == 0:
				clear()
				feedback = ""
			elif navigator == "b" and len(dirContents[bottomPageNumber:topPageNumber]) == 0:
				clear()
				feedback = ""
			# Search function
			elif navigator == "s":
				# Ask for regex pattern, compile it, then iterate through the directory checking to see if notes match. If the notes do match, they're added to a list. At the end of the iterations, set dirContents (the variable used to print contents) equal to the results stored in this list and sort as usual. If there are no matches, re-sort the directory to show all notes again and notify the user. Also set search = True to show the "clear search" option.
				search = True
				regMatchList = []
				searchTerm = str(input(" Enter search term (regex): "))
				clear()
				pattern = re.compile(searchTerm)
				for elem in dirContents:
					match = re.search(pattern, elem)
					if match:
						regMatchList.append(elem)
				dirContents = sorted(regMatchList, key=str.lower)
				if dirContents == []:
					clear()
					feedback = "No notes matching term found."
					search = False
					dirContents = os.listdir()
					holderList = []
					for elem in dirContents:
						isFile = os.path.isfile(elem)
						if isFile == True:
							holderList.append(str(elem))
					dirContents = holderList
					dirContents = sorted(dirContents, key=str.lower)
			# Clear search, redo list
			elif navigator == "c":
				clear()
				feedback = "Search cleared."
				search = False
				dirContents = os.listdir()
				holderList = []
				for elem in dirContents:
					isFile = os.path.isfile(elem)
					if isFile == True:
						holderList.append(str(elem))
				dirContents = holderList
				dirContents = sorted(dirContents, key=str.lower)
			# Note editing
			elif navigator =="e":
				userInput = int(input(" Enter the number of the note to edit: "))
				if 0 <= userInput < len(dirContents):
					editFile = dirContents[userInput]
					editCommand = str(editor + " '" + editFile + "'")
					os.system(editCommand)
					feedback = "Changes saved."
					clear()
				else:
					clear()
					feedback = "Note does not exist."
			elif navigator == "d":
				outOfNotes = False
				userInput = int(input(" Enter the number of the note to delete: "))
				if 0 <= userInput < len(dirContents):
					deleteFile = dirContents[userInput]
					confirmation = input("\x1b[33m" + " Are you sure you want to delete " + deleteFile + "? <y/N>" + "\x1b[0m").lower()
					if confirmation == "y":
						clear()
						os.remove(deleteFile)
						# Yes, these lines pop up several times. It's not a function because it breaks if I do that; it can be identical and have access to all variables and it still breaks. No clue why. I'm sure it'll click someday, or someone who knows more about Python will come up with a way to do it.
						dirContents = os.listdir()
						holderList = []
						for elem in dirContents:
							isFile = os.path.isfile(elem)
							if isFile == True:
								holderList.append(str(elem))
						dirContents = holderList
						dirContents = sorted(dirContents, key=str.lower)
						bottomPageNumber = 0
						topPageNumber = bottomPageNumber + fileCount
						pageCount = 1
						feedback = "Note deleted."
					else:
						clear()
						feedback = "Deletion canceled."
				else:
					clear()
					feedback = "Note does not exist."
			elif navigator == "q":
				clear()
				break
			# Any other cases that the user might manage to come up with.
			else:
				clear()
				feedback = "Invalid entry."

# Note menus and handling.
def noteHandler(workingDir):
	feedback = ""
	username = login.username
	sharedSelection = "0"
	# Set settings
	settingsFile = envHome + '/.pluralnotes' + "/" + username + "/data/settings.txt"
	settings = open(settingsFile, 'r').readlines()
	editor = settings[0].strip()
	fileCount = settings[1].strip()
	showDate = settings[2].strip()
	showUsername = settings[3].strip()
	clear()
	dirChanger(workingDir)
	while sharedSelection != "q":
		print()
		print(" You are here: " + workingDir)
		print(""" What would you like to do?
""")
		print("\x1b[31m" + " 1: Add a new note" + "\x1b[0m")
		print("\x1b[33m" + " 2: View, edit, or delete existing notes" + "\x1b[0m")
		print("\x1b[32m" + " q: Return to main menu" + "\x1b[0m")
		if feedback != "":
			print()
		print("\x1b[33m" + " " + feedback + "\x1b[0m")
		sharedSelection = input(" Enter selection: ").lower()

		if sharedSelection == "1" or sharedSelection == "a":
			feedback = ""
			newFile = input(" Enter note name: ")
			if newFile.isspace() == True or " " in newFile or "\n" in newFile or "\t" in newFile:
				clear()
				feedback = "Note names cannot contain spaces, tabs, or new lines. Please enter a valid note name."
			elif newFile == False or newFile == "":
				clear()
				feedback = "Please enter a note name."
			else:
				sharedDir = envHome + '/.pluralnotes' + '/sharednotes'
				# Use settings to add date and/or username onto file
				if showDate.strip() == "True" or workingDir == sharedDir:
					newdatefile = newFile + "-" + str(todayDate)
					newFile = newdatefile
					sleep(0.05) # Filename improperly created if sleep is not added
				if showUsername.strip() == "True" or workingDir == sharedDir:
					newFile = newFile  + "-" + username
					sleep(0.05) # Filename improperly created if sleep is not added
				newFile = newFile + ".txt"
				clear()
				sleep(0.05) # Filename improperly created if sleep is not added
				editCommand = str(editor + " '" + newFile + "'")
				os.system(editCommand)
				# newFile = newFile  + "-" + username + "-" + todayDate + ".txt"
				# Sign note if requested by appending it onto the end of the file contents.
				print()
				signNameCheck = input(" Would you like to sign your note? <Y/n>").lower()
				if signNameCheck == "y" or signNameCheck == "yes":
					signName = open(newFile, "a")
					signName.write("\n -" + username) # New line helps keep the signature distinct
					signName.close
					clear()
					feedback = "Note signed!"
				else:
					clear()
					feedback = "Note saved!"
		elif sharedSelection == "2" or sharedSelection == "v" or sharedSelection == "e":
			feedback = ""
			# View or edit a note; paginated search
			clear()
			paginateDir(os.path.dirname)
		elif sharedSelection.lower() == "q" or sharedSelection.lower() == "quit" or sharedSelection.lower() == "b":
			# Back to main menu.
			feedback = ""
			clear()
			break
		else:
			clear()
			feedback = "Invalid entry. Please enter 1-5."

def replaceLine(fileName, lineNum, text):
    lines = open(fileName, 'r').readlines()
    lines[lineNum] = text
    out = open(fileName, 'w')
    out.writelines(lines)
    out.close()
