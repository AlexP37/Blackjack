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
deck = testerList = []
delay = 61
result = "bet"
betValue = ""
money = 100

end = cont = bust = stand = fiveUnder = mouseDown = dealerFiveUnder = dealerBust = onPlayButton = blackJack = quiting = False

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
        self.fiveUnder = False
        self.value += self.cards[0].value
        if self.cards[0].name in ["ha","da","ca","sa"]:
            self.aceCount += 1
        if self.cards[-1].name in ["ha","da","ca","sa"]:
            if (self.value + 11) > 21:
                self.value += 1
            else:
                self.value += 11
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
        if len(self.cards) >= 5 and self.value < 21:
            self.fiveUnder = True
            print("THERE IS A DECK UNDER 21 WITH 5, AND IT IS", self.player)
            updateScreen()

 
    def display(self):
        cardsInDeckNames = ""
        coords = (20,245)
        pastFirstIteration = False
        for i in self.cards:
            if self.player == "dealer":
                if pastFirstIteration == False:
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
                self.handText = TextBox(text, 75, coords, self.color)
            else:
                self.handText = TextBox(text, 75, coords, textColor)
        else:
            self.handText = TextBox(text, 75, coords, self.color)

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

def textBoxClearLight(text, size, position, color):
    font = pygame.font.Font('LemonLight.otf', size)
    text = font.render(text, True, color)
    textRect = text.get_rect()
    textRect.center = position
    gameDisplay.blit(text, textRect)

def textBoxClearLeft(text, size, position, color):
    font = pygame.font.Font('LemonMilk.otf', size)
    text = font.render(text, True, color)
    textRect = text.get_rect()
    textRect.midleft = position
    gameDisplay.blit(text, textRect)

def textBoxClearLeftLight(text, size, position, color):
    font = pygame.font.Font('LemonLight.otf', size)
    text = font.render(text, True, color)
    textRect = text.get_rect()
    textRect.midleft = position
    gameDisplay.blit(text, textRect)

def textBoxClearRight(text, size, position, color):
    font = pygame.font.Font('LemonMilk.otf', size)
    text = font.render(text, True, color)
    textRect = text.get_rect()
    textRect.midright = position
    gameDisplay.blit(text, textRect)

def textBoxClearRightLight(text, size, position, color):
    font = pygame.font.Font('LemonLight.otf', size)
    text = font.render(text, True, color)
    textRect = text.get_rect()
    textRect.midright = position
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
    
    if stand == True or bust == True or blackJack == True or fiveUnder:
        hitBox.color = standBox.color = splitBox.color = grey_light

    noteBox.text = ""
    if stand == True:
        noteBox.text = "Stood"
    if blackJack == True:
        noteBox.text = "Blackjack"
    if userHand.fiveUnder == True:
        noteBox.text = "5 Under 21"
    if result != "playing" and result != "bet":
        noteBox.text = result
        hitBox.color = standBox.color = splitBox.color = grey_light

    if result in ["win", "loss", "draw"]:
        if money == 0 and result == "loss":
            if 395 < mx < 1145 and 466 < my < 629:
                textBoxClearLight("OUT OF MONEY", 20, (767, 450), textColor)
                textBoxClear("RESTART", 190, (767, 550), textColor)
            else:
                textBoxClearLight("OUT OF MONEY", 20, (767, 450), textColor)
                textBoxClear("RESTART", 180, (767, 550), textColor)
        else:
            if 511 < mx < 1026 and 466 < my < 629:
                textBoxClear("NEXT", 220, (767, 550), textColor)
            else:
                textBoxClear("NEXT", 200, (767, 550), textColor)
    
    noteBox.display()
    textBoxClearRight("BANK: $" + str(money), 50, (1180,40), textColor)
    if result != "bet" and int(betValue) > 0:
        textBoxClearRightLight("BET: $" + betValue, 30, (1180,80), userHand.color)
    textBoxClearLeftLight("Dealer", 30, (20,45), dealerHand.color)
    textBoxClearLeftLight("Player", 30, (20,190), userHand.color)

    if result == "bet":
        TextBox("??: ?? ??", 75, (20,245), textColor)
        TextBox("??: ?? ??", 75, (20,100), textColor)
    else:
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

while quiting == False:
    userHand = Hand("user")
    dealerHand = Hand("dealer")

    noteBox = TextBox("", 100, (20,400), textColor)
    hitBox = TextBox("Hit", 100, (20,500), textColor)
    standBox = TextBox("Stand", 100, (20,600), textColor)
    splitBox = TextBox("Split", 100, (20,700), textColor)

    updateScreen()
    textBoxClearLeft("Type bet", 100, (20,400), blue)
    betValueColor = green
    while result != "playing":
        clock.tick(60)
        betValueColor = green

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                cont = True
                end = True
                pygame.quit()
                pygame.font.quit()
                quit()
            mx, my = pygame.mouse.get_pos()
            if event.type == pygame.KEYDOWN:
                if chr(event.key).isnumeric():
                    if chr(event.key) != "0" or str(betValue) != "" :
                        betValue += (chr(event.key))
                        updateScreen()
                        textBoxClearLeft("$" + str(betValue), 100, (20,400), betValueColor)
                if event.key == pygame.K_BACKSPACE:
                    betValue = betValue[:-1]
                    updateScreen()
                    if str(betValue) != "":
                        textBoxClearLeft("$" + str(betValue), 100, (20,400), betValueColor)
                    else:
                        textBoxClearLeft("Type bet", 100, (20,400), blue)
                if event.key == pygame.K_RETURN:
                    if betValue != "":
                        if int(betValue) != 0 and int(betValue) <= money:
                            money -= int(betValue)
                            result = "playing"
                            hitBox.color = standBox.color = splitBox.color = textColor
                            updateScreen()
                        else:
                            updateScreen()
                            if str(betValue) != "":
                                textBoxClearLeft("$" + str(betValue), 100, (20,400), betValueColor)
                            else:
                                textBoxClearLeft("Type bet", 100, (20,400), blue)

        if betValue.isnumeric():
            if int(betValue) > money:
                if betValueColor == green:
                    betValueColor = red
                    updateScreen()
                    textBoxClearLeft("$" + str(betValue), 100, (20,400), betValueColor)

        pygame.display.update()
        # print(pygame.mouse.get_pos())

    result = "playing"
    updateScreen()

    while end == False:
        clock.tick(60)
        delay += 1

        for event in pygame.event.get():
            mx, my = pygame.mouse.get_pos()

            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                end = True
                quiting = True
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
            #     hitBox.size = 100
            # else:
            #     hitBox.size = 102

            if 22 > mx or mx > 337 or 555 > my or my > 642:
                standBox.color = textColor
                updateScreen()
                cancelledStand = True
            #     standBox.size = 100
            # else:
            #     standBox.size = 102

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
                    if userHand.value < 21 and stand == False and fiveUnder == False:
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

            if result != "playing" and 411 < mx < 1126 and 466 < my < 629 and event.type == pygame.MOUSEBUTTONUP:
                if money == 0 and result == "loss":
                    money = 100
                end = True

        if userHand.value == 21:
            if blackJack == False:
                delay = -30
            stand = True
            blackJack = True
            updateScreen()
        
        if userHand.fiveUnder == True:
            if stand == False:
                delay = -30  
            stand = True
            if delay == -30:
                updateScreen()
                

        print(str(stand) + "THIS IS STAND!!!!!")

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
                    if (dealerBust == True and bust == True) or (dealerHand.value == userHand.value and userHand.fiveUnder == dealerHand.fiveUnder):
                        dealerHand.color = blue
                        userHand.color = blue
                        result = "draw"
                    elif (dealerBust == False and bust == True) or (dealerHand.value > userHand.value and dealerBust == False and userHand.fiveUnder == False) or (dealerHand.fiveUnder == True and userHand.fiveUnder == False):
                        dealerHand.color = green
                        userHand.color = red
                        result = "loss"
                    elif (dealerBust == True and bust == False) or (dealerHand.value < userHand.value and bust == False) or (dealerHand.fiveUnder == False and userHand.fiveUnder == True):
                        userHand.color = green
                        dealerHand.color = red
                        result = "win"
                updateScreen()

        pygame.display.update()
        # print(pygame.mouse.get_pos())

    if result == "win":
        money += (int(betValue) * 2)
    if result == "draw":
        money += (int(betValue))
    betValue = ""
    result = "bet"
    deck = []
    createDeck()
    random.shuffle(deck)
    delay = 61
    end = cont = bust = stand = mouseDown = userHand.fiveUnder = dealerBust = onPlayButton = blackJack = dealerHand.fiveUnder = False
    cancelledStand = cancelledHit = True

for i in userHand.cards:
    print(i.name)
# Game Over
print("Awaiting End")
pygame.quit()
pygame.font.quit()
quit()