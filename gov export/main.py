import sys
import pygame
from fonts import FontLibrary
from game import GameScreen
from levelselect import LevelSelect
from mainscreen import MainScreen
from screenManager import ScreenManager
from text import Text

pygame.init()

screen = pygame.display.set_mode((933, 600))
pygame.display.set_caption("Party Party")
screenManager = ScreenManager()
fontLibrary = FontLibrary()

fontLibrary.load_fonts()

gameScreen = GameScreen(screenManager, fontLibrary)
mainScreen = MainScreen(screenManager, fontLibrary, gameScreen)
levelSelect = LevelSelect(screenManager, fontLibrary, gameScreen)

clock = pygame.time.Clock()
prevMouseClicked = False

running = True

pygame.mixer.music.load("assets/sounds/wholikestoparty.wav")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(loops=-1)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    dt = clock.get_time()/1000
    mousePos = pygame.mouse.get_pos()
    mouseClicked = pygame.mouse.get_pressed()[0]
    if screenManager.transitioning:
        if screenManager.transition == (0, 1):
            mainScreen.transition01(screen)
            levelSelect.transition01(screen)

        elif screenManager.transition == (1, 0):
            mainScreen.transition10(screen)
            levelSelect.transition10(screen)

        elif screenManager.transition == (1, 2):
            gameScreen.transitionIn(screen)
            levelSelect.transition10(screen)

        elif screenManager.transition == (2, 0):
            mainScreen.transition10(screen)
            gameScreen.transitionOut(screen)

        elif screenManager.transition == (0, 2):
            gameScreen.transitionIn(screen)
            mainScreen.transition01(screen)



    else:
        if screenManager.screen == 0:
            mainScreen.render(screen)
            mainScreen.tick(dt, mousePos, mouseClicked, prevMouseClicked)

        elif screenManager.screen == 1:
            levelSelect.render(screen)
            levelSelect.tick(dt, mousePos, mouseClicked, prevMouseClicked)

        elif screenManager.screen == 2:
            gameScreen.tick(dt, mousePos, mouseClicked, prevMouseClicked)
            gameScreen.render(screen)


    screenManager.tick(dt)

    clock.tick()
    prevMouseClicked = mouseClicked
    pygame.display.update()

pygame.quit()
sys.exit()