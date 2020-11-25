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
darkLightImg = pygame.image.load('darkLightButton.png')

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

diffList = [[15, "passive"], [17, "neutral"], [19, "assertive"]]

end = cont = mouseDown = onPlayButton = quiting = dealerTurn = hand2Turn = False

cancelledStand = cancelledHit = cancelledSplit = cpuTurn = cpuPlayer =True

class Card:
    def __init__(self, suit, name, value, cardType):
        self.suit = suit
        self.name = name
        self.value = value
        self.cardType = cardType

class Hand:
    def __init__(self, player, side, coords):
        self.diff = 1
        self.color = textColor
        self.player = player
        self.side = side
        self.coords = coords
        self.value = 0
        self.aceCount = 0
        self.split = False
        self.bust = False
        self.stand = False
        self.fiveUnder = False
        self.blackJack = False

        self.cards = [deck[0], deck[1]]
        self.value += self.cards[0].value
        deck.remove(deck[0])
        deck.remove(deck[0])

        if self.cards[0].name in ["ah","ad","ac","as"]:
            self.aceCount += 1
        if self.cards[-1].name in ["ah","ad","ac","as"]:
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
        if self.cards[-1].name in ["ah","ad","ac","as"]:
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
        pastFirstIteration = False
        for i in self.cards:
            if self.player == "dealer":
                if pastFirstIteration == False and ((userHand.split == False and userHand.bust == False and userHand.stand == False) or (userHand.split == True and userHand2.bust == False and userHand2.stand == False)):
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
            if userHand.bust == True or userHand.stand == True:
                self.handText = TextBox(text, 75, self.coords, self.color, self.side)
            else:
                self.handText = TextBox(text, 75, self.coords, textColor, self.side)
        elif self.player not in ["user", "user2"]:
            self.handText = TextBox(text, 45, self.coords, self.color, self.side)
        else:
            self.handText = TextBox(text, 75, self.coords, self.color, self.side)

class TextBox:
    def __init__(self, text, size, position, color, side):
        self.text = text
        self.size = size
        self.position = position
        self.color = color
        self.side = side
        self.display()

    def display(self):
        font = pygame.font.Font("LemonMilk.otf", self.size)
        text = font.render(self.text, True, self.color)
        textRect = text.get_rect()
        textRect.midleft = self.position
        if self.side == "right":
            textRect.midright = self.position
        elif self.side == "center":
            textRect.center = self.position
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
    # v = 3
    # s = "d"
    # t = "3"
    # singleCard = Card(s, (t + s), v, t)
    # deck.append(singleCard)

    # v = 3
    # s = "c"
    # t = "3"
    # singleCard = Card(s, (t + s), v, t)
    # deck.append(singleCard)
    for s in suits:
        for t in cardTypes:
            v = valuesForCards[cardTypes.index(t)]
            singleCard = Card(s, (t + s), v, t)
            deck.append(singleCard)

def hitCard(who):
    who.hit()

def displayHand(who):
    who.display()

def updateScreen():
    gameDisplay.fill(backgroundColor)

    gameDisplay.blit(darkLightImg, (1148, 748))

    noteBox.text = ""

    if hand2Turn == True:
        userHand2 == currentPlayerHand
    else:
        userHand == currentPlayerHand
    
    if currentPlayerHand.stand == True or currentPlayerHand.bust == True or currentPlayerHand.blackJack == True or currentPlayerHand.fiveUnder:
        hitBox.color = standBox.color = splitBox.color = grey_light

    if currentPlayerHand.bust == True:
        noteBox.text = "bust"
    if currentPlayerHand.stand == True:
        noteBox.text = "Stood"
    if currentPlayerHand.blackJack == True:
        noteBox.text = "Blackjack"
    if currentPlayerHand.fiveUnder == True:
        noteBox.text = "5 Under 21"
    
    if betValue == "":
        if len(userHand.cards) != 2 or userHand.cards[0].cardType != userHand.cards[1].cardType:
            splitBox.color = grey_light
    else:
        if len(userHand.cards) != 2 or userHand.cards[0].cardType != userHand.cards[1].cardType or (money - int(betValue)) < 0:
            splitBox.color = grey_light

    if result != "playing":
        hitBox.color = standBox.color = splitBox.color = grey_light
        if result != "bet":
            noteBox.text = result
    
    if userHand.split == True:
        if hand2Turn == True and userHand2.bust == False and userHand2.stand == False:
            noteBox.text = ""

    if result in ["win", "loss", "draw"]:
        if money == 0 and result == "loss":
            if 395 < mx < 1145 and 499 < my < 662:
                textBoxClearLight("OUT OF MONEY", 20, (767, 483), textColor)
                textBoxClear("RESTART", 190, (767, 583), textColor)
            else:
                textBoxClearLight("OUT OF MONEY", 20, (767, 483), textColor)
                textBoxClear("RESTART", 180, (767, 583), textColor)
        else:
            if 511 < mx < 1026 and 499 < my < 662:
                textBoxClear("NEXT", 220, (767, 583), textColor)
            else:
                textBoxClear("NEXT", 200, (767, 583), textColor)
    
    noteBox.display()
    textBoxClearRight("BANK: $" + str(money), 50, (1180,40), textColor)
    if result != "bet" and int(betValue) > 0:
        textBoxClearRightLight("BET: $" + betValue, 30, (1180,80), userHand.color)
    textBoxClearLeftLight("Dealer", 30, (20,45), dealerHand.color)
    if cpuPlayer == True:
        textBoxClearRightLight("CPU 1", 30, (1180,170), cpuHand.color)
        textBoxClearRightLight(diffList[cpuHand.diff][1], 15, (1080,170), cpuHand.color)
        textBoxClearRightLight("CPU 2", 30, (1180,270), cpuHand2.color)
        textBoxClearRightLight(diffList[cpuHand2.diff][1], 15, (1080,270), cpuHand2.color)
        textBoxClearRightLight("CPU 3", 30, (1180,370), cpuHand3.color)
        textBoxClearRightLight(diffList[cpuHand3.diff][1], 15, (1080,370), cpuHand3.color)
    textBoxClearLeftLight("Player", 30, (20,190), userHand.color)

    if result != "bet" and int(betValue) > 0 and userHand.split == True:
        textBoxClearRightLight("BET 2: $" + betValue, 30, (1180,115), userHand2.color)

    if result == "bet":
        TextBox("??: ?? ??", 75, (20,245), textColor, "left")
        TextBox("??: ?? ??", 75, (20,100), textColor, "left")
        if cpuPlayer == True:
            for i in [0,1,2]:
                TextBox("??: ?? ?? ", 45, (1195,(100 * i) + 210), textColor, "right")
    else:
        displayHand(userHand)
        displayHand(dealerHand)
        if cpuPlayer == True:
            displayHand(cpuHand)
            displayHand(cpuHand2)
            displayHand(cpuHand3)
        if userHand.split == True:
            displayHand(userHand2)

    hitBox.display()
    standBox.display()
    splitBox.display()
    cpuToggle.display()

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
        mx, my = pygame.mouse.get_pos()
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            cont = True
            end = True
            pygame.quit()
            pygame.font.quit()
            quit()
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
    userHand = Hand("user", "left", (20,245))
    dealerHand = Hand("dealer", "left", (20,100))
    cpuHand = Hand("cpu", "right", (1195,210))
    cpuHand2 = Hand("cpu2", "right", (1195,310))
    cpuHand3 = Hand("cpu3", "right", (1195,410))
    currentPlayerHand = userHand

    noteBox = TextBox("", 100, (20,430), textColor, "left")
    hitBox = TextBox("Hit", 100, (20,530), textColor, "left")
    standBox = TextBox("Stand", 100, (20,630), textColor, "left")
    splitBox = TextBox("Split", 100, (20,730), textColor, "left")
    cpuToggle = TextBox("CPU", 45, (1090,774), textColor, "center")

    print(cpuHand.diff)
    updateScreen()
    textBoxClearLeft("Type Bet", 100, (20,430), blue)
    betValueColor = green
    while result != "playing":
        clock.tick(60)
        betValueColor = green
        print(pygame.mouse.get_pos())
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                cont = True
                end = True
                pygame.quit()
                pygame.font.quit()
                quit()
            mx, my = pygame.mouse.get_pos()

            if 1000 < mx < 1080 and 160 < my < 175 and event.type == pygame.MOUSEBUTTONUP:
                cpuHand.diff += 1
                if cpuHand.diff == 3:
                    cpuHand.diff = 0
                updateScreen()
            elif 1000 < mx < 1080 and 260 < my < 275 and event.type == pygame.MOUSEBUTTONUP:
                cpuHand2.diff += 1
                if cpuHand2.diff == 3:
                    cpuHand2.diff = 0
                updateScreen()
            elif 1000 < mx < 1080 and 360 < my < 375 and event.type == pygame.MOUSEBUTTONUP:
                cpuHand3.diff += 1
                if cpuHand3.diff == 3:
                    cpuHand3.diff = 0
                updateScreen()

            if mx > 1150 and my > 750:
                if darkLightImg != pygame.image.load('darkLightButton2.png'):
                    darkLightImg = pygame.image.load('darkLightButton2.png')
                    updateScreen()
                    if str(betValue) != "":
                        textBoxClearLeft("$" + str(betValue), 100, (20,430), betValueColor)
                    else:
                        textBoxClearLeft("Type Bet", 100, (20,430), blue)
                if event.type == pygame.MOUSEBUTTONUP:
                    list1 = [noteBox, hitBox, standBox, splitBox, dealerHand, userHand, cpuToggle, cpuHand, cpuHand2, cpuHand3]
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
                    if str(betValue) != "":
                        textBoxClearLeft("$" + str(betValue), 100, (20,430), betValueColor)
                    else:
                        textBoxClearLeft("Type Bet", 100, (20,430), blue)
            else:
                if darkLightImg != pygame.image.load('darkLightButton.png'):
                    darkLightImg = pygame.image.load('darkLightButton.png')
                    updateScreen()
                    if str(betValue) != "":
                        textBoxClearLeft("$" + str(betValue), 100, (20,430), betValueColor)
                    else:
                        textBoxClearLeft("Type Bet", 100, (20,430), blue)

            if 1040 < mx < 1140 and my > 750:
                if event.type == pygame.MOUSEBUTTONUP:
                    cpuPlayer = not cpuPlayer
                cpuToggle.size = 50
                updateScreen()
                if str(betValue) != "":
                    textBoxClearLeft("$" + str(betValue), 100, (20,430), betValueColor)
                else:
                    textBoxClearLeft("Type Bet", 100, (20,430), blue)
            elif cpuToggle.size == 50:
                cpuToggle.size = 45
                updateScreen()
                if str(betValue) != "":
                    textBoxClearLeft("$" + str(betValue), 100, (20,430), betValueColor)
                else:
                    textBoxClearLeft("Type Bet", 100, (20,430), blue)

            if event.type == pygame.KEYDOWN:
                if chr(event.key).isnumeric():
                    if (chr(event.key) != "0" or str(betValue) != "") and int(betValue + (chr(event.key))) < 100000:
                        betValue += (chr(event.key))
                        updateScreen()
                        textBoxClearLeft("$" + str(betValue), 100, (20,430), betValueColor)
                if event.key == pygame.K_BACKSPACE:
                    betValue = betValue[:-1]
                    updateScreen()
                    if str(betValue) != "":
                        textBoxClearLeft("$" + str(betValue), 100, (20,430), betValueColor)
                    else:
                        textBoxClearLeft("Type Bet", 100, (20,430), blue)
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
                                textBoxClearLeft("$" + str(betValue), 100, (20,430), betValueColor)
                            else:
                                textBoxClearLeft("Type Bet", 100, (20,430), blue)

        if betValue.isnumeric():
            if int(betValue) > money:
                if betValueColor == green:
                    betValueColor = red
                    updateScreen()
                    textBoxClearLeft("$" + str(betValue), 100, (20,430), betValueColor)

        pygame.display.update()

    result = "playing"
    updateScreen()

    while end == False:
        clock.tick(60)
        delay += 1
        print(str(int(clock.get_fps())))

        currentPlayerHand = userHand
        if hand2Turn == True:
            currentPlayerHand = userHand2

        for event in pygame.event.get():
            mx, my = pygame.mouse.get_pos()

            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                end = True
                quiting = True
                pygame.quit()
                pygame.font.quit()
                quit()

            if userHand.stand == False and userHand.bust == False:
                if 1000 < mx < 1080 and 160 < my < 175 and event.type == pygame.MOUSEBUTTONUP:
                    cpuHand.diff += 1
                    if cpuHand.diff == 3:
                        cpuHand.diff = 0
                    updateScreen()
                elif 1000 < mx < 1080 and 260 < my < 275 and event.type == pygame.MOUSEBUTTONUP:
                    cpuHand2.diff += 1
                    if cpuHand2.diff == 3:
                        cpuHand2.diff = 0
                    updateScreen()
                elif 1000 < mx < 1080 and 360 < my < 375 and event.type == pygame.MOUSEBUTTONUP:
                    cpuHand3.diff += 1
                    if cpuHand3.diff == 3:
                        cpuHand3.diff = 0
                    updateScreen()

            if mx > 1150 and my > 750:
                darkLightImg = pygame.image.load('darkLightButton2.png')
                if event.type == pygame.MOUSEBUTTONUP:
                    list1 = [noteBox, hitBox, standBox, splitBox, dealerHand, userHand, cpuToggle, cpuHand, cpuHand2, cpuHand3]
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
            elif darkLightImg == pygame.image.load('darkLightButton2.png'):
                darkLightImg = pygame.image.load('darkLightButton.png')
                updateScreen()

            if 1040 < mx < 1140 and my > 750:
                if event.type == pygame.MOUSEBUTTONUP:
                    cpuPlayer = not cpuPlayer
                cpuToggle.size = 50
                updateScreen()
            elif cpuToggle.size == 50:
                cpuToggle.size = 45
                updateScreen()

            if (22 > mx or mx > 179 or 485 > my or my > 572) and cancelledHit == False:
                hitBox.color = textColor
                updateScreen()
                cancelledHit = True

            if (22 > mx or mx > 337 or 585 > my or my > 672) and cancelledStand == False:
                standBox.color = textColor
                updateScreen()
                cancelledStand = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if 22 < mx < 179 and 485 < my < 572:
                    hitBox.color = red
                    cancelledHit = False
                elif 22 < mx < 337 and 585 < my < 672:
                    standBox.color = green
                    cancelledStand = False
                elif 22 < mx < 278 and 685 < my < 772 and len(currentPlayerHand.cards) == 2 and currentPlayerHand.split == False and currentPlayerHand.cards[0].cardType == currentPlayerHand.cards[1].cardType and (money - int(betValue)) >= 0:
                    splitBox.color = blue
                    cancelledSplit = False
                updateScreen()

            if event.type == pygame.MOUSEBUTTONUP:
                if 22 < mx < 179 and 485 < my < 572 and cancelledHit == False:
                    if currentPlayerHand.value < 21 and currentPlayerHand.stand == False and currentPlayerHand.fiveUnder == False:
                        hitCard(currentPlayerHand)
                    if currentPlayerHand.value > 21:
                        if currentPlayerHand.bust == False:
                            delay = 0
                        currentPlayerHand.bust = True
                elif 22 < mx < 337 and 585 < my < 672 and cancelledStand == False:
                    if currentPlayerHand.stand == False:
                        delay = 0
                    currentPlayerHand.stand = True
                elif 22 < mx < 278 and 685 < my < 772:
                    if len(userHand.cards) == 2 and userHand.cards[0].cardType == userHand.cards[1].cardType and (money - int(betValue)) >= 0 and hand2Turn == False:
                        userHand.split = True
                        money -= int(betValue)
                        userHand2 = Hand("user2", "left", (20,315))
                        userHand2.cards = [userHand.cards[1]]
                        userHand.cards.remove(userHand.cards[1])
                        userHand.value = userHand.cards[0].value
                        userHand2.value = userHand2.cards[0].value
                        if userHand2.cards[0].cardType == "a":
                            userHand2.aceCount -= 1
                            userHand.aceCount -= 1
                        userHand2.color = grey_light

                hitBox.color = textColor
                standBox.color = textColor
                updateScreen()

            if result != "playing" and 411 < mx < 1126 and 469 < my < 662 and event.type == pygame.MOUSEBUTTONUP:
                if money == 0 and result == "loss":
                    money = 100
                end = True

        if currentPlayerHand.value == 21:
            if currentPlayerHand.blackJack == False:
                delay = -30
            currentPlayerHand.stand = True
            currentPlayerHand.blackJack = True
            updateScreen()
        
        if currentPlayerHand.fiveUnder == True:
            if currentPlayerHand.stand == False:
                delay = -30  
            currentPlayerHand.stand = True
            if delay == -30:
                updateScreen()

        if userHand.split == False:
            if userHand.bust == True or userHand.stand == True:
                dealerTurn = True
        else:
            if (userHand2.bust == True or userHand2.stand == True):
                dealerTurn = True
            if (userHand.bust == True or userHand.stand == True) and delay >= 30 and hand2Turn == False:
                userHand.color = grey_light
                userHand2.color = textColor
                hand2Turn = True
                hitBox.color = textColor
                standBox.color = textColor
                currentPlayerHand = userHand2
                updateScreen()
                delay = 61

        if dealerTurn == True:
            if cpuTurn == True and cpuPlayer == True:
                if cpuHand.color != textColor:
                    cpuHand.color = textColor
                    updateScreen()
                    delay = 30
                if delay > 60:
                    for cpuHittingHand in [cpuHand, cpuHand2, cpuHand3]:
                        if cpuHittingHand.value > 21:
                            cpuHittingHand.bust = True
                        elif cpuHittingHand.value >= diffList[cpuHittingHand.diff][0]:
                            cpuHittingHand.stand = True
                        elif len(cpuHittingHand.cards) >= 5 and cpuHittingHand.value < 21:
                            cpuHittingHand.fiveUnder = True
                            cpuHittingHand.stand = True
                        else:
                            hitCard(cpuHittingHand)
                        i = cpuHittingHand
                    updateScreen()
                    if (cpuHand.stand == True or cpuHand.bust == True) and (cpuHand2.stand == True or cpuHand2.bust == True) and (cpuHand3.stand == True or cpuHand3.bust == True):
                        cpuTurn = False
                    delay = 0
            else:
                if dealerHand.value > 21:
                    dealerHand.bust = True
                if len(dealerHand.cards) >= 5 and dealerHand.value < 21:
                    dealerHand.fiveUnder = True
                    dealerHand.stand = True
                if delay > 60:
                    delay = 0
                    if dealerHand.value < 17 and dealerHand.fiveUnder == False:
                        hitCard(dealerHand)
                        if dealerHand.value > 21:
                            dealerHand.bust = True
                    else:
                        for handChecking in [cpuHand, cpuHand2, cpuHand3, userHand]:
                            if (dealerHand.value == handChecking.value and handChecking.fiveUnder == dealerHand.fiveUnder):
                                dealerHand.color = blue
                                handChecking.color = blue
                                result = "draw"
                            elif (dealerHand.bust == False and handChecking.bust == True) or (dealerHand.value > handChecking.value and dealerHand.bust == False and handChecking.fiveUnder == False) or (dealerHand.fiveUnder == True and handChecking.fiveUnder == False) or (dealerHand.bust == True and handChecking.bust == True):
                                dealerHand.color = green
                                handChecking.color = red
                                result = "loss"
                            elif (dealerHand.bust == True and handChecking.bust == False) or (dealerHand.value < handChecking.value and handChecking.bust == False) or (dealerHand.fiveUnder == False and handChecking.fiveUnder == True):
                                handChecking.color = green
                                dealerHand.color = red
                                result = "win"
                            
                            if handChecking.player == "user":
                                userHand = handChecking
                            elif handChecking.player == "cpu":
                                cpuHand = handChecking
                            elif handChecking.player == "cpu2":
                                cpuHand2 = handChecking
                            else:
                                cpuHand3 = handChecking
                            
                            if handChecking.split == True:
                                if (dealerHand.bust == True and userHand2.bust == True) or (dealerHand.value == userHand2.value and userHand2.fiveUnder == dealerHand.fiveUnder):
                                    userHand2.color = blue
                                    result2 = "draw"
                                elif (dealerHand.bust == False and userHand2.bust == True) or (dealerHand.value > userHand2.value and dealerHand.bust == False and userHand2.fiveUnder == False) or (dealerHand.fiveUnder == True and userHand2.fiveUnder == False):
                                    userHand2.color = red
                                    result2 = "loss"
                                elif (dealerHand.bust == True and userHand2.bust == False) or (dealerHand.value < userHand2.value and userHand2.bust == False) or (dealerHand.fiveUnder == False and userHand2.fiveUnder == True):
                                    userHand2.color = green
                                    result2 = "win"
                                
                                if result != result2:
                                    dealerHand.color = blue
                    updateScreen()
                if result != "playing":
                    updateScreen()

        pygame.display.update()

    if result == "win":
        money += (int(betValue) * 2)
    if result == "draw":
        money += (int(betValue))
    if userHand.split == True:
        if result2 == "win":
            money += (int(betValue) * 2)
        if result2 == "draw":
            money += (int(betValue))
    betValue = ""
    result = "bet"
    deck = []
    createDeck()
    random.shuffle(deck)
    delay = 61
    end = cont = userHand.bust = userHand.stand = mouseDown = hand2Turn = userHand.fiveUnder = dealerHand.bust = onPlayButton = userHand.blackJack = dealerHand.fiveUnder = userHand.split = dealerTurn = False
    cancelledStand = cancelledHit = cancelledSplit = cpuTurn = True


# Game Over
print("Awaiting End")
pygame.quit()
pygame.font.quit()
quit()