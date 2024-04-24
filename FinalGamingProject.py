# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 09:36:27 2024

@author: Ryan Miller
"""

import pygame, random
import simpleGE

class BSUcard (simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("Cardinal.png")
        self.setSize(90,50)
        self.position = (300,400)
        self.moveSpeed = 7
        self.inAir = True
        
    def process(self):
        if self.inAir:
            self.addForce(.2, 270)
        
        if self.y > 450:
            self.inAir = False
            self.y = 450
            self.dy = 0
        
        if self.isKeyPressed(pygame.K_LEFT):
            self.x -= self.moveSpeed
        if self.isKeyPressed(pygame.K_RIGHT):
            self.x += self.moveSpeed
        if self.isKeyPressed(pygame.K_UP):
            if not self.inAir:
                self.addForce(8, 90)
                self.inAir = True
                
        self.inAir = True
        for platform in self.scene.platforms:
            if self.collidesWith(platform):                
                if self.dy > 0:
                        self.bottom = platform.top
                        self.dy = 0
                        self.inAir = False
                        
class Platform(simpleGE.Sprite):
    def __init__(self, scene, position):
        super().__init__(scene)
        self.position = (position)
        self.colorRect("darkblue", (50, 50))
       
    
        
class coin(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("coin.gif")
        self.setSize(20,20)
        self.reset()
        
    def Bounds(self):
        if self.bottom > self.screenHeight:
            self.reset()
            
        
    def reset(self):
      self.y = 12
      self.x = random.randint(0, self.screenWidth)
      self.dy = random.randint(3, 8)
      
class Introscene(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.setImage("Campus.jpg")
        self.instructions =simpleGE.MultiLabel()
        self.instructions.textLines = ["Ball State Jump","Instructions:","The goal is to Collect as many coins as you can","Key controls:",'Use button "<" "^" ">" to move',]
        self.instructions.size = (500,300)
        self.instructions.center = (320,240)
        self.sprites = [self.instructions]
        self.response = ""
        
    def process(self):
        if self.instructions.clicked:
            self.response = "Play"
            self.stop()
    
    
            
class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.setImage("BSU_tower.jpg")
        self.sndcoin = simpleGE.Sound("Coin_sound.wav")
        self.setCaption("arrows to move and jump. drag platforms around")
        self.sndBSUcard = simpleGE.Sound("Boing.mp3")

        self.platforms = [Platform(self, (100, 450)), 
                          Platform(self, (150, 450)), 
                          Platform(self, (200, 450)), 
                          Platform(self, (250, 450)),
                          Platform(self, (300, 350)), 
                          Platform(self, (350, 350))]
       
        self.score = 0
        self.timer = simpleGE.Timer()
        self.timer.totalTime = 30
        self.timeLabel = timeLabel()
        
        self.BSUcard = BSUcard(self)
        
        self.coinScore = coinScore()
        
        self.coin = []
        for i in range(3):
            self.coin.append(coin(self))
            
        self.sprites = [self.BSUcard,
                        self.coin,
                        self.timeLabel,
                        self.platforms,
                        self.coinScore]
                        
        
        
    def process(self):
      
        for coin in self.coin:
            if self.BSUcard.collidesWith(coin):
                self.sndcoin.play()
                self.coinScore = 1

                coin.reset() 
        
        self.timeLabel.text = f"Time Left: {self.timer.getTimeLeft():.2f}"
        if self.timer.getTimeLeft() < 0:
            print(f"Score: {self.score}")
            self.stop()
                
class timeLabel(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Time Left: 30"
        self.center = (80,20)
        self.size = (170,40)
        
class coinScore(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Score: 0"
        self.center = (575,15)
        
       
def main():
    
    intro = Introscene()
    intro.start()
    
    if intro.response == "Play":
        game = Game()
        game.start()
    
    
if __name__ == "__main__":
    main()