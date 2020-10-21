# Initialization of Game
import os
import pygame
import math
import random

os.system("clear")

pygame.init()
pygame.font.init()
display_width = 750
display_height = 750
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
blue = (0,0,255)
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Blackjack')
clock = pygame.time.Clock()
gameDisplay.fill((255,255,255))

suits = ["h","d","c","s"]
cardTypes = ["a","2","3","4","5","6","7","8","9","10","j","q","k"]
valuesForCards = [1,2,3,4,5,6,7,8,9,10,10,10,10]

deck = []
hand = []
testerList = []

class Card:
    def __init__(self, suit, name, value, cardType):
        self.suit = suit
        self.name = name
        self.value = value
        self.cardType = cardType

class Hand:
    def __init__(self):
        self.value = 0
        self.cards = [deck[0], deck[1]]
        deck.remove(deck[0])
        deck.remove(deck[0])
        for i in self.cards:
            self.value += int(self.cards[self.cards.index(i)].value)

    def hit(self):
        self.cards.append(deck[0])
        deck.remove(deck[0])
        self.value = 0
        for i in self.cards:
            self.value += int(self.cards[self.cards.index(i)].value)

def createDeck():
    for s in suits:
        for t in cardTypes:
            v = valuesForCards[cardTypes.index(t)]
            singleCard = Card(s, (s + t), v, t)
            deck.append(singleCard)

def hitCard(who):
    who.hit()

createDeck()
random.shuffle(deck)
userHand = Hand()
dealerhand = Hand()

end = False
while end == False:
    clock.tick(60)
    hitCard(userHand)



for i in userHand.cards:
    print(userHand.cards[userHand.cards.index(i)].name)
# Game Over
print("Awaiting End")
pygame.quit()
pygame.font.quit()
quit()