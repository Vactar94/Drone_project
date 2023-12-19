import pygame
import sys

def init():
    pygame.init()
    win = pygame.display.set_mode((400, 400))


def getKey(keyName):
    ans=False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    KeyInput = pygame.key.get_pressed()
    myKey = getattr(pygame, "K_{}".format(keyName))
    if KeyInput[myKey]:
        ans = True
    pygame.display.update()
    return ans

def main():
    if getKey("LEFT"):
        print("GAUCHE a été pressé")
    if getKey("RIGHT"):
        print("DROITE a été pressé")

        

if __name__ == "__main__":
    init()
    while True:
        main()