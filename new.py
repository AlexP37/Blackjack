# Initialization of Game
import os
import pygame
import math
import random

os.system("clear")

pygame.init()
pygame.font.init()

red = redOG = (165,0,0)
green = greenOG = (0,165,0)
blue = blueOG = (0,0,165)
backgroundColor = whiteOG = (255,255,255)
textColor = blackOG = (0,0,0)
grey_light = grey_lightOG = (210,210,210)

display_width = 1200
display_height = 800
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Blackjack')
clock = pygame.time.Clock()
gameDisplay.fill(backgroundColor)

suits = ["h","d","c","s"]
cardTypes = ["a","2","3","4","5","6","7","8","9","10","j","q","k"]
valuesForCards = [11,2,3,4,5,6,7,8,9,10,10,10,10]
deck = hand = testerList = []
delay = 61
result = "bet"

end = cont = bust = stand = mouseDown = dealerBust = onPlayButton = blackJack = False

cancelledStand = cancelledHit = True

class Card:
    def __init__(self, suit, name, value, cardType):
        self.suit = suit
        self.name = name
        self.value = value
        self.cardType = cardType

class Hand:
    def __init__(self, player):
        self.color = textColor
        self.player = player
        self.value = 0
        self.aceCount = 0
        self.cards = [deck[0], deck[1]]
        deck.remove(deck[0])
        deck.remove(deck[0])
        self.value += self.cards[0].value
        if self.cards[-1].name in ["ha","da","ca","sa"] and (self.value + 11) > 21:
            self.value += 1
            self.aceCount += 1
        else:
            self.value += self.cards[-1].value

    def hit(self):
        self.cards.append(deck[0])
        deck.remove(deck[0])
        if self.cards[-1].name in ["ha","da","ca","sa"]:
            self.aceCount += 1
        self.value += self.cards[-1].value
        if self.value > 21:
            if self.aceCount > 0:
                self.aceCount -= 1
                self.value -= 10
 
    def display(self):
        cardsInDeckNames = ""
        coords = (20,200)
        pastFirstIteration = False
        for i in self.cards:
            if self.player == "dealer":
                if pastFirstIteration == False :
                    coords = (20,100)
                if pastFirstIteration == False and bust == False and stand == False:
                    cardsInDeckNames += "?? "
                    text = "??: " + cardsInDeckNames
                else:
                    cardsInDeckNames += i.name + " "
                    if pastFirstIteration == False:
                        text = str(self.value) + ": " + cardsInDeckNames
                    else:
                        text += i.name + " "
            else:
                cardsInDeckNames += i.name + " "
                text = str(self.value) + ": " + cardsInDeckNames
            pastFirstIteration = True
        if self.player == "dealer":
            if bust == True or stand == True:
                self.handText = TextBox(text, 50, coords, self.color)
            else:
                self.handText = TextBox(text, 50, coords, textColor)
        else:
            self.handText = TextBox(text, 50, coords, self.color)

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
    textRect.center = position
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
    gameDisplay.fill(backgroundColor)
    
    # if stand == True:
    #     hitBox.color = standBox.color = splitBox.color = grey_light
    # if bust == True:
    #     hitBox.color = standBox.color = splitBox.color = grey_light

    noteBox.text = ""
    if bust == True:
        noteBox.text = "Bust"
    if stand == True:
        noteBox.text = "Stood"
    if blackJack == True:
        noteBox.text = "Blackjack"
    if result != "playing":
        noteBox.text = result
        hitBox.color = standBox.color = splitBox.color = grey_light
    
    noteBox.display()
    displayHand(userHand)
    displayHand(dealerHand)
    # betBox.display()
    hitBox.display()
    standBox.display()
    splitBox.display()

createDeck()
random.shuffle(deck)

gameDisplay.fill(backgroundColor)
pygame.draw.rect(gameDisplay, (5,5,5), (600, 0, 600, 800))
textBoxClear("Light", 100, (300,400), textColor)
textBoxClear("Dark", 100, (900,400), (255,255,255))
while cont == False:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            cont = True
            end = True
            pygame.quit()
            pygame.font.quit()
            quit()
        mx, my = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 600 < mx:
                textColor = (255,255,255)
                backgroundColor = (5,5,5)
                green = (0,120,0)
                red = (120,0,0)
                blue = (0,0,120)
                grey_light = (100,100,100)
            cont = True
    pygame.display.update()

cont = False
gameDisplay.fill(backgroundColor)
textBoxClear("Play", 300, (display_width / 2, display_height / 2), textColor)
while cont == False:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            cont = True
            end = True
            pygame.quit()
            pygame.font.quit()
            quit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            if backgroundColor != (5,5,5):
                textColor = (255,255,255)
                backgroundColor = (5,5,5)
                green = (0,120,0)
                red = (120,0,0)
                blue = (0,0,120)
                grey_light = (100,100,100)
            else:
                textColor = blackOG
                backgroundColor = whiteOG
                green = greenOG
                red = redOG
                blue = blueOG
                grey_light = grey_lightOG
        mx, my = pygame.mouse.get_pos()
        if 245 < mx < 967 and 277 < my < 529:
            gameDisplay.fill(backgroundColor)
            textBoxClear("Play", 320, (display_width / 2, display_height / 2), textColor)
            if event.type == pygame.MOUSEBUTTONDOWN or mouseDown == True:
                onPlayButton = True
                mouseDown = True
                gameDisplay.fill(backgroundColor)
                textBoxClear("Play", 320, (display_width / 2, display_height / 2), green)
            if event.type == pygame.MOUSEBUTTONUP and mouseDown == True:
                if onPlayButton == True:
                    cont = True
                mouseDown = False
                gameDisplay.fill(backgroundColor)
        else:
            gameDisplay.fill(backgroundColor)
            textBoxClear("Play", 300, (display_width / 2, display_height / 2), textColor)
        if event.type == pygame.MOUSEBUTTONUP and mouseDown == True:
            onPlayButton = False
            mouseDown = False
    pygame.display.update()

userHand = Hand("user")
dealerHand = Hand("dealer")

noteBox = TextBox("Bust", 100, (20,400), textColor)
hitBox = TextBox("Hit", 100, (20,500), textColor)
standBox = TextBox("Stand", 100, (20,600), textColor)
splitBox = TextBox("Split", 100, (20,700), textColor)

updateScreen()
while result == "bet":
    clock.tick(60)
    for event in pygame.event.get():
        mx, my = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 20 < mx < 200 and 355 < my < 445:
                noteBox.color = blue
                updateScreen()
            
        if event.type == pygame.MOUSEBUTTONUP:
            if 20 < mx < 200 and 355 < my < 445:
                result = "playing"
                noteBox.color = textColor
                hitBox.color = standBox.color = splitBox.color = textColor
                updateScreen()

    pygame.display.update()
    print(pygame.mouse.get_pos())

result = "playing"

while end == False:
    clock.tick(60)
    delay += 1

    for event in pygame.event.get():
        mx, my = pygame.mouse.get_pos()

        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            end = True
            pygame.quit()
            pygame.font.quit()
            quit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            list1 = [noteBox, hitBox, standBox, splitBox, dealerHand, userHand]
            if backgroundColor != (5,5,5):
                textColor = (255,255,255)
                backgroundColor = (5,5,5)
                green = (0,120,0)
                red = (120,0,0)
                blue = (0,0,120)
                grey_light = (100,100,100)
                for i in list1:
                    if i.color == blackOG:
                        i.color = textColor
            else:
                for i in list1:
                    if i.color != blackOG:
                        i.color = blackOG
                textColor = blackOG
                backgroundColor = whiteOG
                green = greenOG
                red = redOG
                blue = blueOG
                grey_light = grey_lightOG
            updateScreen()


        if 22 > mx or mx > 179 or 455 > my or my > 542:
            hitBox.color = textColor
            updateScreen()
            cancelledHit = True
            hitBox.size = 100
        else:
            hitBox.size = 102

        if 22 > mx or mx > 337 or 555 > my or my > 642:
            standBox.color = textColor
            updateScreen()
            cancelledStand = True
            standBox.size = 100
        else:
            standBox.size = 102

        if event.type == pygame.MOUSEBUTTONDOWN:
            if 22 < mx < 179 and 455 < my < 542:
                hitBox.color = red
                cancelledHit = False
            elif 22 < mx < 337 and 555 < my < 642:
                standBox.color = green
                cancelledStand = False
            elif 22 < mx < 278 and 655 < my < 742:
                print("lmao")
            updateScreen()

        if event.type == pygame.MOUSEBUTTONUP:
            if 22 < mx < 179 and 455 < my < 542 and cancelledHit == False:
                if userHand.value < 21:
                    hitCard(userHand)
                if userHand.value > 21:
                    if bust == False:
                        delay = 0
                    bust = True
            elif 22 < mx < 337 and 555 < my < 642 and cancelledStand == False:
                if stand == False:
                    delay = 0
                stand = True
            hitBox.color = textColor
            standBox.color = textColor
            updateScreen()

    if userHand.value == 21:
        if blackJack == False:
            delay = -30
        stand = True
        blackJack = True
        updateScreen()

    if bust == True or stand == True:
        if dealerHand.value > 21:
            dealerBust = True
        if delay > 60:
            if dealerHand.value < 17:
                delay = 0
                hitCard(dealerHand)
                if dealerHand.value > 21:
                    dealerBust = True
            if dealerHand.value >= 17:
                if (dealerBust == True and bust == True) or (dealerHand.value == userHand.value):
                    dealerHand.color = blue
                    userHand.color = blue
                    result = "draw"
                elif (dealerBust == False and bust == True) or (dealerHand.value > userHand.value and dealerBust == False):
                    dealerHand.color = green
                    userHand.color = red
                    result = "loss"
                elif (dealerBust == True and bust == False) or (dealerHand.value < userHand.value and bust == False):
                    userHand.color = green
                    dealerHand.color = red
                    result = "win"
            updateScreen()
    pygame.display.update()
    print(pygame.mouse.get_pos())
    

for i in userHand.cards:
    print(i.name)
# Game Over
print("Awaiting End")
pygame.quit()
pygame.font.quit()
quit()