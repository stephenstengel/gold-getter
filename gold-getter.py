#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  GoldGetter.py
#  
#  Copyright 2018 Stephen Stengel <stephen.stengel@cwu.edu>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

#STEPHEN STENGEL
#CS565 project 2


#This is a small game where the player gets the gold and avoids the bomb.

#Controls: 	Move player with WASD.

#TODO:
#		19 oct 2020: Rewrite to use classes because I know this stuff now.
#
#		Use copyright free art! So I can put it on github
#
#		More bombs. Read array for all, move each one at a time.
#
#		Add proximity to chase mechanic. Only chase when within two squares?
#
#		Just figured out how to add bombs. Make the detection functions put
#		coordinates into a tuple and pass that. Obviously change things to look
#		for more bombs. Best would be a variable amount of bombs.
#
#		Add intellegence to bomb movements.  STARTED
#
#		Add more bombs/difficulties.
#
#		Make it so bombs cannot kill before player moves.
#
#		Czech spellingz
#
#		Prevent user from making the board too small or too big
#
#		Figure out what I meant by some of these comments...
#
#		If I ever need to change the function createDataArray(), give it better 
#		variable names.
#
#		Also I could simplify createDataArray() by just using the isPlayerHere, 
#		isBombHere, and isgoldhere functions etc. instead of checking 
#		coordinates manually.
#

#DONE:
#		Fix the bug where an endless loop is started if the bomb starts the game
#		boxxed in a corner by two golds.  DONE
#
#		Add ability to control player.  DONE
#
#		Find a way to prevent the jumpy graphics glitch.  DONE
#
#		Make it so that it doesn't exit on win/loss. Instead go into loop using
#		input and print.  DONE

#IDEAS:
#		Keep player from moving more than two squares away from the bomb.
#
#		If bomb finds gold, it should puppyguard the gold.
#
#		Add obsticals (if no path between player and gold retry. same for bomb)


import random
import readchar
import math
import pygame


pygame.init()


#Global variables because I'm literally just slapping this together in like an hour.
SCREEN_SIZE = 640
WINDOW_BOARD_DIMENSION = 5

WINDOW = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Gold Getter")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Images
PLAYER_IMAGE = pygame.transform.scale(pygame.image.load("images/robot.png").convert(), (80, 80))
BOMB_IMAGE = pygame.transform.scale(pygame.image.load("images/bomb.png").convert(), (80, 80))
GOLD_IMAGE = pygame.transform.scale(pygame.image.load("images/gold.png").convert(), (80, 80))


class SquareStatus(object):
	def __init__(self, isBombHere, isPlayerHere, \
					wasBombHere, wasPlayerHere, isGoldHere):
		self.isBombHere = isBombHere
		self.isPlayerHere = isPlayerHere
		self.wasBombHere = wasBombHere
		self.wasPlayerHere = wasPlayerHere
		self.isGoldHere = isGoldHere
		
class Engine(object):
	def __init__(self):
		pass
		
	def API(self):
		DIMENSION = self.BOARD_DIMENSION()
		WINDOW_BOARD_DIMENSION = DIMENSION
		theBoardYo = self.createDataArray(DIMENSION)
		self.playGame(theBoardYo, DIMENSION)
		
	#Use this to pass the value of the size of the board to functions
	#Call the created variable DIMENSION inside of the function
	#Don't make the board 1x1, lol
	#We can change the size of the board by changing the number that is returned
	def BOARD_DIMENSION(self):
		size = input(\
			"What size should the square board be?\n"\
			"Enter an integer from 3 to 9.\n"\
			"(If you are in fullscreen try 3 to 19): ")
		return int(size)
		
	
	#This creates the data array that holds the places of the characters and
	#generates the initial positions of the caracters
	def createDataArray(self, DIMENSION):
		#print("Creating the game board array that stores the data...")
		boardArray = \
					[[SquareStatus( False, \
									False, \
									False, \
									False, \
									False) for x in range(DIMENSION)] \
													for y in range(DIMENSION)]
		#print("boardArray created!")
		
		#sets player's initial position
		(a, b) = self.randomStart(DIMENSION)
		boardArray[a][b].isPlayerHere = True
		
		#sets bomb's initial position. Repeats if spot is taken.
		(c, d) = self.randomStart(DIMENSION)
		while(c == a and d == b):
			(c, d) = self.randomStart(DIMENSION)
		boardArray[c][d].isBombHere = True
		
		#sets golds initial position.
		(e, f) = self.randomStart(DIMENSION)
		while((e == c and f == d) or (e == a and f == b)):
			(e, f) = self.randomStart(DIMENSION)
		boardArray[e][f].isGoldHere = True
		
		#sets another gold.
		(g, h) = self.randomStart(DIMENSION)
		while(     (g == e and h == f) \
				or (g == c and h == d) \
				or (g == a and h == b)    ):
			(g, h) = self.randomStart(DIMENSION)
		boardArray[g][h].isGoldHere = True
		
		return boardArray


	#This function contains the loop that runs the game.
	def playGame(self, boardArray, DIMENSION):
		updatedBoardArray = boardArray	
		print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
		isStillGold = self.isThereStillGold(updatedBoardArray, DIMENSION)
		self.displayBoard(updatedBoardArray, DIMENSION)
		throwAwayVariable = ""
		throwAwayVariable = print(input("press enter key to continue!"))
		while(isStillGold):
			#make bomb walk once#doing this after player
			updatedBoardArray = self.moveBomb(updatedBoardArray, DIMENSION)
			print(	"\n\n\n\n\n\n\n\n\n\n\n\n\n" \
					"\n\n\n\n\n\n\n\n\n\n\n\n\n" \
					"Avoid the bomb!")
			self.displayBoard(updatedBoardArray, DIMENSION)
			#throwAwayVariable = print(input("press enter key to continue!"))
			
			#check if bomb is on player
			#tested working
			if(self.isBombOnPlayer(updatedBoardArray, DIMENSION)):
				print(  "OWCH!\n" + \
						"The bomb got you!\n" + \
			"I don't care what universe you're from-- that's gotta hurt!\n" +\
						"GAME OVER!\n")
				exit(0)
				
			#make player walk
		#	print("\n\n\n\n\n\n\n\n\n\n\n\n\nPlayer's turn...")
			updatedBoardArray = \
							 self.movePlayerManual(updatedBoardArray, DIMENSION)
			#playerongold?
			if(self.isPlayerOnGold(updatedBoardArray, DIMENSION)):
				(a, b) = self.getPlayerPosition(updatedBoardArray, DIMENSION)
				self.deleteGold(updatedBoardArray, DIMENSION, a, b)
			print(	"\n\n\n\n\n\n\n\n\n\n\n\n\n" \
					"\n\n\n\n\n\n\n\n\n\n\n\n\n" \
					"Avoid the bomb!")
			self.displayBoard(updatedBoardArray, DIMENSION)
			#throwAwayVariable = print(input("press enter key to continue!"))
			
			#check if bomb is on player
			#tested working
			if(self.isBombOnPlayer(updatedBoardArray, DIMENSION)):
				print(  "OWCH!\n" + \
						"The bomb got you!\n" + \
			"I don't care what universe you're from-- that's gotta hurt!\n" +\
						"GAME OVER!\n")
				exit(0)
			
			#check if there is any gold left
			isStillGold = self.isThereStillGold(updatedBoardArray, DIMENSION)
			if(isStillGold != True):
				break
			
			#make player walk again
			updatedBoardArray = \
							 self.movePlayerManual(updatedBoardArray, DIMENSION)
			#playerongold?
			if(self.isPlayerOnGold(updatedBoardArray, DIMENSION)):
				(a, b) = self.getPlayerPosition(updatedBoardArray, DIMENSION)
				self.deleteGold(updatedBoardArray, DIMENSION, a, b)
			print(	"\n\n\n\n\n\n\n\n\n\n\n\n\n" \
					"\n\n\n\n\n\n\n\n\n\n\n\n\n" \
					"Player's turn...")
			self.displayBoard(updatedBoardArray, DIMENSION)
			#throwAwayVariable = print(input("press enter key to continue!"))
			
			#check if bomb is on player
			#tested working
			if(self.isBombOnPlayer(updatedBoardArray, DIMENSION)):
				print(  "OWCH!\n" + \
						"The bomb got you!\n" + \
			"I don't care what universe you're from-- that's gotta hurt!\n" +\
						"GAME OVER!\n")
				exit(0)
			
			#check if there is any gold left
			isStillGold = self.isThereStillGold(updatedBoardArray, DIMENSION)
			if(isStillGold != True):
				break
				
		print("You got all the gold! YAAAAAAAAAY!")
	

	def displayBoard(self, boardArray, DIMENSION):
		#print("Displaying board...")
		print("##################")
		the_underscores = "_"
		print(" " + \
				str(the_underscores * (  (DIMENSION * 3) + (DIMENSION - 1)  ) ))
				
		for i in range(DIMENSION):
			for j in range(DIMENSION):
				print("| " \
							+ self.displayCharacters(boardArray, i, j) \
							+ " ", end = '')
			print("|\n ", end = "")
			print(the_underscores * (  (DIMENSION * 3) + (DIMENSION - 1)  ) )
		#for underscores we need DIMENSION*3 + (DIMENSION - 1) underscores
		#print("Done!")
		
		## New bit to display the board with pygame. I'm going to just
		## read the array every time that this is called and use a
		## couple for loops to fill the screen.
		
		WINDOW.fill(WHITE)
		unitSize = SCREEN_SIZE // WINDOW_BOARD_DIMENSION
		
		#Start points for drawing lines
		x = 0
		for i in range(WINDOW_BOARD_DIMENSION):
			x = i * unitSize
			pygame.draw.line(WINDOW, BLACK, (x, 0), (x, SCREEN_SIZE), 1)
			pygame.draw.line(WINDOW, BLACK, (0, x), (SCREEN_SIZE, x), 1)
		
		# I need to get the position in which to place each image.
		x = y = 0
		for i in range(len(boardArray)):
			for j in range(len(boardArray[i])):
				if boardArray[i][j].isPlayerHere:
					x = i * unitSize
					y = j * unitSize
					WINDOW.blit(PLAYER_IMAGE, (x,y) )
				if boardArray[i][j].isBombHere:
					x = i * unitSize
					y = j * unitSize
					WINDOW.blit(BOMB_IMAGE, (x,y) )
				if boardArray[i][j].isGoldHere:
					x = i * unitSize
					y = j * unitSize
					WINDOW.blit(GOLD_IMAGE, (x,y) )
				
		#add footprints later
		
		# ~ self.isBombHere = isBombHere
		# ~ self.isPlayerHere = isPlayerHere
		# ~ self.wasBombHere = wasBombHere
		# ~ self.wasPlayerHere = wasPlayerHere
		# ~ self.isGoldHere = isGoldHere
		
		# ~ # Drawing X's and O's
	    # ~ for image in images:
	        # ~ x, y, IMAGE = image
	        # ~ win.blit(IMAGE, (x - IMAGE.get_width() // 2, y - IMAGE.get_height() // 2))

		pygame.display.update()
		
	#This function needs to return characters with a priority of:
	#bomb, player, gold, bombtrail, playertrail
	def displayCharacters(self, boardArray, i, j):
		if(boardArray[i][j].isBombHere):
			return "B"
		elif(boardArray[i][j].isPlayerHere):
			return "P"
		elif(boardArray[i][j].isGoldHere):
			return "G"
		elif(boardArray[i][j].wasBombHere):
			return ","
		elif(boardArray[i][j].wasPlayerHere):
			return "."
		else:
			return " "
		
		
	def randomStart(self, DIMENSION):
		i = -1.0
		j = -1.0
		i = random.randint(0, DIMENSION - 1)
		j = random.randint(0, DIMENSION - 1)
		#print("This is i:" + str(i))
		#print("This is j:" + str(j))
		return (i, j)


	#Checks the boardArray for gold
	def isThereStillGold(self, boardArray, DIMENSION):
		#print("isThereStillGold has been called")
		for i in range(DIMENSION):
			for j in range(DIMENSION):
				if(boardArray[i][j].isGoldHere):
					return True
		return False
		
		
	#checks if bomb is on the player
	def isBombOnPlayer(self, boardArray, DIMENSION):
		if(self.getPlayerPosition(boardArray, DIMENSION) \
					== self.getBombPosition(boardArray, DIMENSION)):
			return True
		return False
	
	
	#returns the cell that the player is in as a tuple
	def getPlayerPosition(self, boardArray, DIMENSION):
		i = -1
		j = -1
		for i in range(DIMENSION):
			for j in range(DIMENSION):
				if(boardArray[i][j].isPlayerHere):
					return (i, j)
		return (i, j)
		
		
	#returns the cell that the bomb is in as a tuple
	def getBombPosition(self, boardArray, DIMENSION):
		i = -1
		j = -1
		for i in range(DIMENSION):
			for j in range(DIMENSION):
				if(boardArray[i][j].isBombHere):
					return (i, j)
		return (i, j)


	#Why is it called IF?
	def checkIfGoldPosition(self, boardArray, DIMENSION):
		i = -1
		j = -1
		for i in range(DIMENSION):
			for j in range(DIMENSION):
				if(boardArray[i][j].isBombHere):
					return (i, j)
		return (i, j)

				
	#Move the player! Manually!
	def movePlayerManual(self, boardArray, DIMENSION):
		(currentY, currentX) = self.getPlayerPosition(boardArray, DIMENSION)
		(finalY, finalX) = (currentY, currentX)
				
		#this section ayy
		while( (finalY, finalX) == (currentY, currentX) ):
			#print("Which way do you want to go?!")
			wayToGo = "q"
			while( (wayToGo != "w") \
					and (wayToGo != "a") \
					and (wayToGo != "s") \
					and (wayToGo != "d") ):
				wayToGo = readchar.readchar()
			if(wayToGo == "w"):#up
				#print("up")
				(y, x) = ((currentY - 1), currentX)
			#	print("y of proposed position " + str(y))
			#	print("x of proposed position " + str(x))
			elif(wayToGo == "a"):#left
				#print("left")
				(y, x) = (currentY,(currentX - 1))
			#	print("y of proposed position " + str(y))
			#	print("x of proposed position " + str(x))
			elif(wayToGo == "d"):#right
				#print("right")
				(y, x) = (currentY, (currentX + 1))
			#	print("y of proposed position " + str(y))
			#	print("x of proposed position " + str(x))
			elif(wayToGo == "s"):#down
				#print("down")
				(y, x) = ((currentY + 1), currentX)
			#	print("y of proposed position " + str(y))
			#	print("x of proposed position " + str(x))
				
			#wait! just return the one thing that you want changed and 
			#change/set it in the game function?
			#Not sure what that comment was supposed to mean.
			if(self.checkIfCanMovePlayer(boardArray, DIMENSION, y, x)):
				boardArray[currentY][currentX].isPlayerHere = False
				boardArray[currentY][currentX].wasPlayerHere = True
			#	print("boardArray[currY][currX].isPlayerHere: " \
			#		+ str(boardArray[currentY][currentX].isPlayerHere))
				boardArray[y][x].isPlayerHere = True
			#	print("boardArray[y][x].isPlayerHere: " \
			#		+ str(boardArray[y][x].isPlayerHere))
				(finalY, finalX) = (y, x)
			#	print("returnning boardArray")
				return boardArray
		
	#Checks proposed movement for validity.
	def checkIfCanMovePlayer(self, boardArray, DIMENSION, y, x):
		if(y < 0):
			return False
		elif(y > DIMENSION - 1):
			return False
		elif(x < 0):
			return False
		elif(x > DIMENSION - 1):
			return False
		#this would be too easy
		#~ elif((y, x) == self.getBombPosition(boardArray, DIMENSION)):
			#~ return False
		else:
			return True

		
	#I need to make the bomb smarter.
	#Add a thing to check bomb's y,x position compared to player position
	#Make bomb only able to reduce distance between it and player.
	#Maybe just put this in the canBombMove function? Then don't need to change
	#anything here and it will just get sent back here to roll again.
	#	Might need to add a counter loop to prevent getting stuck behind an
	#	obstical. Or just add a don't move condition?
	#Need a new function to check the distance between the bomb and the player
	#	Could just use standard distance formula from algebra?
	def moveBomb(self, boardArray, DIMENSION):
		(currentY, currentX) = self.getBombPosition(boardArray, DIMENSION)
		(finalY, finalX) = (currentY, currentX)
		(playerY, playerX) = self.getPlayerPosition(boardArray, DIMENSION)
		#print("Player is at..." + str(playerY) + ", " + str(playerX))
		print("bomb distance: " \
				+ str(self.bombDistance(playerY, playerX, currentY, currentX)) )
		
		#stuckCounter is how many times the bomb has tried and failed to move.
		#The bomb will not move if it hits 50.
		stuckCounter = 0
		while( ((finalY, finalX) == (currentY, currentX)) \
						and (stuckCounter < 50) ):
							
			num = random.uniform(0.0, 1.0)
			if(num < 0.25):#up
		#		print("up")
				(y, x) = ((currentY - 1), currentX)
		#		print("y of proposed position " + str(y))
		#		print("x of proposed position " + str(x))
			elif(num < 0.5):#left
		#		print("left")
				(y, x) = (currentY,(currentX - 1))
		#		print("y of proposed position " + str(y))
		#		print("x of proposed position " + str(x))
			elif(num < 0.75):#right
		#		print("right")
				(y, x) = (currentY, (currentX + 1))
		#		print("y of proposed position " + str(y))
		#		print("x of proposed position " + str(x))
			else:#down
		#		print("down")
				(y, x) = ((currentY + 1), currentX)
		#		print("y of proposed position " + str(y))
		#		print("x of proposed position " + str(x))
			#throoooow = print(input("heh"))
			
			#distance checks
			currentBombDistance = self.bombDistance(playerY, \
													playerX, \
													currentY, \
													currentX)
			proposedBombDistance = self.bombDistance(playerY, playerX, y, x)

			if(self.checkIfCanMoveBomb(boardArray, \
									   DIMENSION, \
									   y, \
									   x, \
									   currentBombDistance, \
									   proposedBombDistance)):
				#print("running the second if in moveBomb...")
				boardArray[currentY][currentX].isBombHere = False
				boardArray[currentY][currentX].wasBombHere = True
			#	print("boardArray[currY][currX].isBombHere: " \
			#			+ str(boardArray[currentY][currentX].isBombHere))
				boardArray[y][x].isBombHere = True
			#	print("boardArray[y][x].isBombHere: " \
			#			+ str(boardArray[y][x].isBombHere))
				(finalY, finalX) = (y, x)
			#	print("returnning boardArray")
				return boardArray
			stuckCounter += 1
		return boardArray
				
				
	def checkIfCanMoveBomb(self, \
						   boardArray, \
						   DIMENSION, \
						   y, \
						   x, \
						   currentBombDistance, \
						   proposedBombDistance):
		if(y < 0):
			return False
		elif(y > DIMENSION - 1):
			return False
		elif(x < 0):
			return False
		elif(x > DIMENSION - 1):
			return False
		elif(boardArray[y][x].isGoldHere):
			return False
		elif(proposedBombDistance > currentBombDistance):
			return False
		else:
			return True
	
	#Returns the direct distance between the player and bomb.
	def bombDistance(self, playerY, playerX, bombY, bombX):
		return math.sqrt( (playerX - bombX)**2 + (playerY - bombY)**2 )
			
	
	def isPlayerOnGold(self, boardArray, DIMENSION):#THIS FIRST HAAHA
		(a, b) = self.getPlayerPosition(boardArray, DIMENSION)
		if(boardArray[a][b].isGoldHere):
		#	print("player IS on gold!")
			return True
		else:
		#	print("player is NOT on gold")
			return False


	#Deletes a gold!? Call Greenspan!
	def deleteGold(self, boardArray, DIMENSION, a, b):
		boardArray[a][b].isGoldHere = False


def main():
	e = Engine()
	e.API()
	pass

if __name__ == '__main__':
	main()



################################################################################
#old movePlayer function
#~ #player will not move onto bomb
	#~ #if cannot move in first direction, it must re-roll
	#~ #(y, x) is the way it is set up now
	#~ #WORKS still need to change old place to False
	#~ #also need to fix the weird error that it gives about line 176
	#~ #maybe change the recursion to a while loop!
	
	#~ #The player starts at the same place each time the loop is run! NOT GOOD
	#~ def movePlayer(self, boardArray, DIMENSION):
		#~ (currentY, currentX) = self.getPlayerPosition(boardArray, DIMENSION)
		#~ (finalY, finalX) = (currentY, currentX)
		
		#~ #print("y of current position " + str(currentY))
		#~ #print("x of current position " + str(currentX))
		#~ # ~ (y, x) = ((a -1), b)
		#~ # ~ print("y of proposed position" + str(y))
		#~ # ~ print("x of proposed position" + str(x))
		
		#~ while( (finalY, finalX) == (currentY, currentX) ):
			#~ num = random.uniform(0.0, 1.0)
			#~ if(num < 0.25):#up
			#~ #	print("up")
				#~ (y, x) = ((currentY - 1), currentX)
			#~ #	print("y of proposed position " + str(y))
			#~ #	print("x of proposed position " + str(x))
			#~ elif(num < 0.5):#left
			#~ #	print("left")
				#~ (y, x) = (currentY,(currentX - 1))
			#~ #	print("y of proposed position " + str(y))
			#~ #	print("x of proposed position " + str(x))
			#~ elif(num < 0.75):#right
			#~ #	print("right")
				#~ (y, x) = (currentY, (currentX + 1))
			#~ #	print("y of proposed position " + str(y))
			#~ #	print("x of proposed position " + str(x))
			#~ else:#down
			#~ #	print("down")
				#~ (y, x) = ((currentY + 1), currentX)
			#~ #	print("y of proposed position " + str(y))
			#~ #	print("x of proposed position " + str(x))
				
			#~ #wait! just return the one thing that you want changed and change/set it in the game function?
			#~ if(self.checkIfCanMovePlayer(boardArray, DIMENSION, y, x)):
				#~ boardArray[currentY][currentX].isPlayerHere = False
				#~ boardArray[currentY][currentX].wasPlayerHere = True
			#~ #	print("boardArray[currY][currX].isPlayerHere: " + str(boardArray[currentY][currentX].isPlayerHere))
				#~ boardArray[y][x].isPlayerHere = True
			#~ #	print("boardArray[y][x].isPlayerHere: " + str(boardArray[y][x].isPlayerHere))
				#~ (finalY, finalX) = (y, x)
			#~ #	print("returnning boardArray")
				#~ return boardArray
