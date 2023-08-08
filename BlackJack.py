from random import shuffle, uniform, randint
import os
	
class Card:
	symbols = ["spades", "clubs", "hearts", "diamonds"]
	values = [
		"ace", "two", "three", "four", "five", "six",
		"seven", "eight", "nine", "ten", "jack", "queen",
		"king", "joker"
	]
	
	asciiSyms = "SHDC"
	asciiValues = "A.2.3.4.5.6.7.8.9.10.J.Q.K.#".split('.')
	
	values = {
		"A": 1,
		"2": 2,
		"3": 3,
		"4": 4,
		"5": 5,
		"6": 6,
		"7": 7,
		"8": 8,
		"9": 9,
		"10": 10,
		"J": 11,
		"Q": 12,
		"K": 13,
		"#": 100,
	}
	
	back = [
		",,,,,,,",
		"|×/C\\×|",
		"|/ A \\|",
		"|\\ R /|",
		"|×\\D/×|",
		"```````",
	]
	
	def __init__(self, value, symbol):
		if (not value in range(1, 15, 1)):
			raise ValueError("value must be in range 1 - 14")
		
		if (not symbol in range(0, 4, 1)):
			raise ValueError("value must be in range 0 - 3")
		
		self.symbol = Card.symbols[symbol]
		
		self.num = Card.asciiValues[value - 1]
		self.value = Card.values[self.num]
		
		self.ascii = Card.asciiSyms[symbol]
		
		self.asciiArt = self.__draw__()
		self.faceUp = False
	
	def flip(self):
		if (self.faceUp):
			self.faceUp = False
		else:
			self.faceUp = True
		
	def __draw__(self):
		art = [
			",,,,,,,",
			f"|{self.num:2}  {self.ascii}|",
			f"|/{self.ascii}{self.num:>2}\\|",
			f"|\\{self.num:2}{self.ascii}/|",
			f"|{self.ascii}  {self.num:>2}|",
			"```````",
		]
		return art
	
	def __str__(self):
		if (self.faceUp):
			return "\n".join(self.asciiArt)
		
		return "\n".join(Card.back)

class Deck(list):
	def __init__(self, empty = False, preShuffle = False):
		super().__init__()
		
		if (not empty):
			for sym in range(0, 4, 1):
				for val in range(1, 14, 1):
					self.add(Card(val, sym))
	
		if (preShuffle):
			shuffle(self)
	
	def draw(self):
		return self.pop()
	
	def add(self, card):
		self.append(card)
		
	def rowStr(self, cardsPerRow = 5):
		out = ""
		if (len(self) > 0):
			i = 0
			r = len(self) % cardsPerRow
			
			for x in range(len(self) // cardsPerRow):
				for y in range(len(self[0].asciiArt)):
					for card in range(i, i + cardsPerRow):
						if (self[card].faceUp):
							out += self[card].asciiArt[y] + " "
						else:
							out += Card.back[y] + " "
					
					out += "\n"
				
				out += "\n"
				i += cardsPerRow
			
			for y in range(len(self[0].asciiArt)):
				for card in range(i, i + r):
					if (self[card].faceUp):
						out += self[card].asciiArt[y] + " "
					else:
						out += Card.back[y] + " "
						
				out += "\n"
		
		return out
		
	def __str__(self):
		out = ""
		for card in self:
			out += str(card) + "\n"
		
		return out
	
class Hand(Deck):
	def __init__(self):
		super().__init__(empty = True)
	
class Player:
	def __init__(self, name = "Player"):
		self.name = name
		
		self.score = 0
		self.hand = Hand()

		self.revealed = False
	
	def draw(self, deck, amount = 2):
		for x in range(amount):
			deck = self.hitMe(deck)
		
		return deck
	
	def hitMe(self, deck):
		card = deck.draw()
		card.flip()
		self.score += card.value
		self.hand.add(card)
		
		return deck
	
	def reveal(self):
		self.revealed = True
		return self.hand.rowStr(8)
	
	def update(self, deck):
		return deck
	
	def __str__(self):
		out = f"\nYour hand | Score: {self.score}\n"
		return out + self.hand.rowStr(8)

class AI(Player):
	def update(self, deck):
		confidence = self.score / 21
		choice = uniform(confidence / 2, 1)
		
		if (choice < confidence or self.score >= 21):
			self.reveal()
			
		else:
			deck = self.hitMe(deck)
		
		if (self.score >= 21):
			self.reveal()
		
		return deck
	
	def __str__(self):
		return f"AI - {self.name:15} | revealed: {str(self.revealed):5}| Score: {'?' if (not self.revealed) else self.score}"

class Players(dict):
	def __init__(self, *players):
		super().__init__()
		
		for player in players:
			self[player.name] = player
	
	def getWinners(self):
		winners = []
		for _, player in self.items():
			if (player.score <= 21):
				winners.append(player)
		
		winner = winners[0]
		for player in winners:
			if (player.score > winner.score):
				winner = player
		
		return winner
	
	def gameOver(self):
		count = 0
		for _, player in self.items():
			if (player.revealed):
				count += 1
		
		if (count == len(self) or self.__weHaveAWinner__()):
			return True
		
		return False
		
	def add(self, player):
		self[player.name] = player
	
	def draw(self, deck, amount = 2):
		for _, player in self.items():
			for x in range(amount):
				deck = player.hitMe(deck)
		
		return deck
	
	def update(self, deck):
		for _, player in self.items():
			if (not player.revealed):
				deck = player.update(deck)
		
		return deck
	
	def __weHaveAWinner__(self):
		for _, player in self.items():
			if (player.score == 21):
				return True
		
		return False
		
	def __str__(self):
		out = ""
		for _, player in self.items():
			out += str(player) + "\n"
		
		return out
	
def clear():
	if (os.name in ['nt', 'dos']):
		os.system('cls')
	else:
		os.system('clear')
	
def game(names):
	deck = Deck(preShuffle=True)
	players = Players()
	
	for x in range(4):
		players.add(AI(names[randint(0, len(names) - 1)]))
		
	players.add(Player())
	
	deck = players.draw(deck, 2)
	
	while (not players.gameOver()):
		clear()
		
		#Player update
		if (players['Player'].score > 21):
			players['Player'].reveal()
			print(f"Deck Remaining: {len(deck):2}\n"+"\n".join(Card.back), "\n")
	
			print(players)
	
		else:
			validInput = False
			while (not validInput):
				clear()
				print(f"Deck Remaining: {len(deck):2}\n"+"\n".join(Card.back), "\n")
	
				print(players)
				print("What would you like to do(hit/reveal)?")
	
				move = input(">>")
				if (move == "hit"):
					deck = players['Player'].hitMe(deck)
					validInput = True
	
				elif (move == "reveal"):
					players['Player'].reveal()
					validInput = True
	
				else:
					print("Unrecognized command. Please try again.")
					input("Press enter to continue...\n>>")
		
		#AI Update
		deck = players.update(deck)
	
	clear()
	print(f"Deck Remaining: {len(deck):2}\n"+"\n".join(Card.back), "\n")
	print(players)
	
	winner = players.getWinners()
	if (winner.name == 'Player'): 
		print(f"You won with a score of {winner.score}!")
	else:
		print(f"You lost to {winner.name} with a score of {winner.score}!")
	
	yn = input("Would you like to play again(y/n)?\n>>")
	if (yn == "n"):
		return False
	
	return True
	
if __name__ == "__main__":
	from random import seed
	from time import time
	import sys
	
	names = "Quagmire.Brian.Louis Griffon.Peter Griffon.Stan Smith.Francine Smith.Jordan Shanks.Mark Fishbauch.Roger.Steven.Pearl.Hank Hill.Peggy Hill.Dale Gribble.John Redcorne.Redneck Joe.Boomhauer".split('.')
	
	seed(time())
	
	if (len(sys.argv) > 0 and sys.argv[0] == True):
		raise NotImplementedError("Gui not implemented")
		
	else:
		playing = True
		while (playing):
			clear()
			playing = game(names)
			
	print("Thanks for playing.")