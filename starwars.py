#####################################################################
# This program is free software. It comes without any warranty, to  #
# the extent permitted by applicable law. You can redistribute it   #
# and/or modify it under the terms of the Do What The Fuck You Want #
# To Public License, Version 2, as published by Sam Hocevar. See    #
# http://sam.zoy.org/wtfpl/COPYING for more details.                #
# A copy of the license should be in this folder                    #
# under the name LICENSE                                            #
#####################################################################

######################## IMPORT AND GLOBALS #########################
#Import stuff:
import random #for creating random integers
import time	#for the intro
import tkinter as tk #for the keyboard events.
from pygame import mixer	#for sound
#Unfortunately, I found no good way to do this without this external library
#Since tkinter works platformwide, I used it

#Global variables:
playerchr="v"	#The character used to display the player
playerpos=0	#The starting position (at the left)
areasize=50	#The width of the game area
arealen=14	#The height of the game area.
#This could be as big as we wanted to, however, for
#performance reasons it should be kept small

obstacles=[]	#The list in which the obstacles/the main game area are stored
clear = (" "*areasize)	#I define a string of spaces that is as long as the game area
count=0		#For various reasons, the "frames" are counted
score=0		#The score starts with zero and increases as the game passes
#antirandomness=1	#I called this value "antirandomness" because the bigger
#it gets, the less "random" will the area become: It will produce a higher amount of
#obstacles, see makepseudorandomline()

activegame=True	#I use this to stop the after() call when losing
paused=False	#self-explanatory
delay=100	#In the beginning, between each frame there is a 1/10s break.
crawl=[]
welcome_message='''STAR WARS EPISODE VII

by Jonathan Oberlaender
jober@coli.uni-saarland.de

Licenced under WTFPL in 2011'''

#Now: The intro string
introframes = ['''
#############################################
''',
'''
 #############################################
#           S T A R   W A R S               #
''',
'''
  #############################################
 #           S T A R   W A R S               #
# Controls:                                 #
''',
'''
   #############################################
  #           S T A R   W A R S               #
 # Controls:                                 #
#            A, D:    Move left, right      #
''',
'''
    #############################################
   #           S T A R   W A R S               #
  # Controls:                                 #
 #            A, D:    Move left, right      #
#               S:    Move to center        #
''',
'''
     #############################################
    #           S T A R   W A R S               #
   # Controls:                                 #
  #            A, D:    Move left, right      #
 #               S:    Move to center        #
#               P:    Pause game            #
''',
'''
      #############################################
     #           S T A R   W A R S               #
    # Controls:                                 #
   #            A, D:    Move left, right      #
  #               S:    Move to center        #
 #               P:    Pause game            #
#          Escape:    Exit game             #
''',
'''
       #############################################
      #           S T A R   W A R S               #
     # Controls:                                 #
    #            A, D:    Move left, right      #
   #               S:    Move to center        #
  #               P:    Pause game            #
 #          Escape:    Exit game             #
#############################################
''',
'''
       #############################################
       #           S T A R   W A R S               #
      # Controls:                                 #
     #            A, D:    Move left, right      #
    #               S:    Move to center        #
   #               P:    Pause game            #
  #          Escape:    Exit game             #
 #############################################
''',
'''
       #############################################
       #           S T A R   W A R S               #
       # Controls:                                 #
      #            A, D:    Move left, right      #
     #               S:    Move to center        #
    #               P:    Pause game            #
   #          Escape:    Exit game             #
  #############################################
''',
'''
       #############################################
       #           S T A R   W A R S               #
       # Controls:                                 #
       #            A, D:    Move left, right      #
      #               S:    Move to center        #
     #               P:    Pause game            #
    #          Escape:    Exit game             #
   #############################################
''',
'''
       #############################################
       #           S T A R   W A R S               #
       # Controls:                                 #
       #            A, D:    Move left, right      #
       #               S:    Move to center        #
      #               P:    Pause game            #
     #          Escape:    Exit game             #
    #############################################
''',
'''
       #############################################
       #           S T A R   W A R S               #
       # Controls:                                 #
       #            A, D:    Move left, right      #
       #               S:    Move to center        #
       #               P:    Pause game            #
      #          Escape:    Exit game             #
     #############################################
''',
'''
       #############################################
       #           S T A R   W A R S               #
       # Controls:                                 #
       #            A, D:    Move left, right      #
       #               S:    Move to center        #
       #               P:    Pause game            #
       #          Escape:    Exit game             #
      #############################################
''',
'''
       #############################################
       #           S T A R   W A R S               #
       # Controls:                                 #
       #            A, D:    Move left, right      #
       #               S:    Move to center        #
       #               P:    Pause game            #
       #          Escape:    Exit game             #
       #############################################
'''
]

######################## FUNCTIONS ##################################

def intro():
	"""Prints the hardcoded intro"""
	for i in range(0,15):	#print ALL the lines
		print("\n"*25)	#clear screen
		print(welcome_message)	#Welcome user
		print(introframes[i])	#print one frame
		time.sleep(0.25)	#wait for 250ms
	input("Press enter to start game")	#wait for user input


def splitHighscoreEntry(strng):
	"""Splits a line of the highscore file to name and score"""
	splitted=strng.split(" ")
	if len(splitted) != 2:	#if the line contains anything but something matching this: /^[^ ] [^ ]$/, it's corrupted
		print("Corrupt highscore file. (len:" + str(len(splitted)) + "), string:" + strng)
		exit()	#to fix a corrupted file, edit it by hand.
	else:
		return [splitted[0],int(splitted[1])]	#return a list of the name and the score

def getPlayerName():
	"""Gets a valid player name from stdin"""
	name=None
	while name==None:
		name=input("Enter your name (alphanumerical, no spaces):")
		if " " in name:	#if space is in the name, try again.
			name=None
	return name

def makepseudorandomline():
	"""Generates the next line of text"""
	global areasize	#appearantly, we have to declare a variable as global in every function
	#to be able to use it
	
	chr=""	#Start with an empty string
	while len(chr) != areasize:
		if len(chr) > areasize-7:
			chr+=crawl[areasize-len(chr)-1][random.randint(0,len(crawl[areasize-len(chr)-1])-1)]
			break
		r = random.randint(0,6)
		chr += crawl[r][random.randint(0,len(crawl[r])-1)]
		chr += " "
	return chr + " "

def step():
	"""The main function to generate frames, called by Tkinter's mainloop"""
	global areasize, clear, obstacles, count, score, playerpos, delay, activegame, paused	#use globals	
	if paused:	#if the user is in pause mode:
		root.after(1000, step)	#longer time delay here to save processing time
		return None	#return for not updating the screen
	print("\n"*20)	#print 20 empty lines to clear the screen
	if count % 10 == 0:	#we only do stuff every tenth step. This enables the player to move faster than the game proceeds
		removed=obstacles.pop(0)	#remove the line that is the closest to the player
		#if removed[(playerpos+1) % areasize] != " " and removed[(playerpos+1) % areasize] != "v":	#look for obstacle at the current player position
		if removed[(playerpos) % areasize] != " " and removed[(playerpos) % areasize] != "v":	#look for obstacle at the current player position
			print("ASDNKASDAS:",removed[(playerpos+1)])
			root.destroy()	#Exit the mainloop of tkinter, destroy the input window and do the stuff that is proceeded by the "Finally"
			#comment in this file
			activegame=False	#This one is for root.after() not to be called
		if count % 30 == 0:	#Every 30th frame (every 3rd area change):
			obstacles.append(" " + makepseudorandomline())	#insert new obstacle line
			score += 1	#increase score
		else:
			obstacles.append(clear)	#otherwise insert "empty" line
	#print(" " * (playerpos),playerchr)	#print player at designated position
	currentline=obstacles[0]
	print(currentline[:(playerpos)] + playerchr + currentline[playerpos+1:])
	for i in range(1,arealen):	#print all lines, obstacle-containing or not
		print(obstacles[i])
	if (count+1) % 300 == 0:	#every 500th frame (every 50th area):
		delay = int(delay * 0.7) #increase speed. This formula ensures the delay never reaches zero and reduces slower after time
	#if (count+1) % 800 == 0:	#every 800th frame (every 80th area):
	#	antirandomness +=1 #increase antirandomness (number of obstacles)
	#Next line: Print status information
	print("SCORE: " + str(score) + " POS: " + str(playerpos+1) + " STEP " + str(count) + " DELAY " + str(delay))	# + " LEVEL " + str(antirandomness))
	count+=1	#increase frame counter
	if activegame:	#only call root.after() if the game is still active
		root.after(delay, step)	#register new function call after the delay time
 
def keypress(event):
	"""The function to be called whenever a key event occures"""
	global areasize, playerpos,paused	#use globals
	if event.keysym == 'Escape':	#Escape instantly ends the game
		root.destroy()
		exit("No copyright (WTFPL) 2011, Jonathan Oberlaender <jober@coli.uni-saarland.de>")
	x = event.char	#otherwise read key character
	if x == "p":#toggle pause
		print("\n"*25)	#clear screen: no speed pausing!
		print("[GAME PAUSED]")
		paused = not paused	#toggle
	elif x == "d":
		playerpos = (playerpos +1) % areasize	#increase player position, modulo areasize (for obvious reasons)
	elif x == "s":
		playerpos = areasize//2-1	#center player
	elif x == "a":
		playerpos = (playerpos -1) % areasize	#decrease player position, modulo areasize

def splitcrawlline(line):
	l = []
	for word in line.split(" "):
		l.append(word.rstrip())
	return l

######################## MAIN PART BEFORE GAME ######################

for i in range(0,arealen-4):
	obstacles.append(clear)	#fill initial obstacle list
obstacles.append("      STAR WARS EPISODE VII - The dark terminal        ")	#fill initial obstacle list
obstacles.append(clear)
obstacles.append(clear)
obstacles.append(clear)

#intro()	#call intro function	

mixer.pre_init()	#initialise mixer
mixer.init(44100,-16,2,4096)
if mixer.get_init():
	bgmusic = mixer.Sound("bg.ogg")	#play background music
	bgmusic.play()

with open("crawl.txt") as f:	#fill crawl
	for line in f:
		crawl.append(splitcrawlline(line))

######################## TKINTER INITIALISATION #####################

root = tk.Tk()	#initialize Tkinter
root.bind_all('<Key>', keypress)	#bind ALL the keys!
# don't show the tk window
#root.withdraw()	#commented out because this makes problems under Linux


root.after(1000, step)	#Initially give the user more time than usual; to read the Welcome message and prepare
root.mainloop()	#TO THE MAINLOOP!!!

######################## AFTER THE GAME #############################

#Finally:
print("\n" * 25)	#Clear the screen
print("YOU LOST THE GAME.")	#Display goodbye message

highscores=[]	#start with empty list
with open("scores.list") as f:	#fill it from lines of the highscore file
	for line in f:
		highscores.append(line)

for i in range(0,len(highscores)):
	highscores[i] = splitHighscoreEntry(highscores[i])	#split into [string,int] lists and check validity

for i in range(0,len(highscores)):
	if int(score) > int(highscores[i][1]):	#if our score is better than one of the ones in the highscore file,
		name=getPlayerName()	#get our player's name
		highscores.pop()	#remove the last (worst) highscore
		highscores.insert(i,[name,score])	#and insert our score in place (sort of "insertsorty")
		break	#but no doubles please

print("\n")
print("HIGHSCORES:")	#eventually print highscore list
with open("scores.list","w") as f:	#and write new highscores to file
	for entry in highscores:
		f.write(entry[0] + " " + str(entry[1]) + "\n")
		print(entry[0] + "\t" + str(entry[1]))
print("No copyright (WTFPL) 2011, Jonathan Oberlaender <jober@coli.uni-saarland.de>")

######################## END OF SCRIPT ##############################
