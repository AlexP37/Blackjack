# Initialization of Game
import os
import pygame
import math
import random

os.system("clear")

pygame.init()
pygame.font.init()
display_width = 1200
display_height = 800
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Blackjack')
clock = pygame.time.Clock()
gameDisplay.fill((255,255,255))

suits = ["h","d","c","s"]
cardTypes = ["a","2","3","4","5","6","7","8","9","10","j","q","k"]
valuesForCards = [11,2,3,4,5,6,7,8,9,10,10,10,10]

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
    def __init__(self, player):
        self.player = player
        self.value = 0
        self.cards = [deck[0], deck[1]]
        deck.remove(deck[0])
        deck.remove(deck[0])
        self.value += self.cards[0].value
        if self.cards[-1].name in ["ha","da","ca","sa"] and (self.value + 11) > 21:
            self.value += 1
        else:
            self.value += self.cards[-1].value

    def hit(self):
        self.cards.append(deck[0])
        deck.remove(deck[0])
        if self.cards[-1].name in ["ha","da","ca","sa"] and (self.value + 11) > 21:
            self.value += 1
        else:
            self.value += self.cards[-1].value
 
    def display(self):
        cardsInDeckNames = ""
        coords = (20,200)
        for i in self.cards:
            cardsInDeckNames += i.name + " "
        if self.player == "dealer":
            coords = (20,100)
        textBoxClear(str(self.value) + ": " + cardsInDeckNames, 50, coords, (0,0,0))

class TextBox:
    def __init__(self, text, size, position, color):
        self.text = text
        self.size = size
        self.position = position
        self.color = color
        self.display()

    def display(self):
        font = pygame.font.Font("LemonMilk.otf", self.size)
        text = font.render(self.text, True, self.color)
        textRect = text.get_rect()
        textRect.midleft = self.position
        gameDisplay.blit(text, textRect)
        self.rect = textRect

def textBoxClear(text, size, position, color):
    font = pygame.font.Font('LemonMilk.otf', size)
    text = font.render(text, True, color)
    textRect = text.get_rect()
    textRect.midleft = position
    gameDisplay.blit(text, textRect)

def createDeck():
    for s in suits:
        for t in cardTypes:
            v = valuesForCards[cardTypes.index(t)]
            singleCard = Card(s, (s + t), v, t)
            deck.append(singleCard)

def hitCard(who):
    who.hit()

def displayHand(who):
    who.display()

def updateScreen():
    gameDisplay.fill((255,255,255))
    if stand == True:
        standBox.color = (0,165,0)
    displayHand(userHand)
    displayHand(dealerHand)
    # betBox.display()
    hitBox.display()
    standBox.display()
    splitBox.display()

createDeck()
random.shuffle(deck)

userHand = Hand("user")
dealerHand = Hand("dealer")

# betBox = TextBox("Bet", 100, (20,400), (0,0,0))
hitBox = TextBox("Hit", 100, (20,500), (0,0,0))
standBox = TextBox("Stand", 100, (20,600), (0,0,0))
splitBox = TextBox("Split", 100, (20,700), (0,0,0))

end = False
bust = False
stand = False

updateScreen()

while end == False:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end = True
            pygame.quit()
            pygame.font.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                end = True
                pygame.quit()
                pygame.font.quit()
                quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if hitBox.rect.collidepoint(mx, my):
                hitBox.color = (165,0,0)
                if userHand.value < 21:
                    hitCard(userHand)
                if userHand.value > 21:
                    bust = True
            elif standBox.rect.collidepoint(mx, my):
                stand = True
            elif splitBox.rect.collidepoint(mx, my):
                print("lmao")
            updateScreen()
        if event.type == pygame.MOUSEBUTTONUP:
            mx, my = pygame.mouse.get_pos()
            if hitBox.rect.collidepoint(mx, my):
                hitBox.color = (0,0,0)
            updateScreen()
    if bust == True or stand == True:
        if dealerHand.value < 17:
            hitCard(dealerHand)
            updateScreen()
    pygame.display.update()

for i in userHand.cards:
    print(i.name)
# Game Over
print("Awaiting End")
pygame.quit()
pygame.font.quit()
quit()