import loader
from simulator import Simulator
from text import Text


class MainScreen:
    def __init__(self, screenManager, fontLibrary, gameScreen):
        self.screenManager = screenManager
        self.tutorial = loader.load_image("tutorial")
        self.freeplay = loader.load_image("freeplay")

        self.tT = Text("Tutorial", fontLibrary.heading, (255, 255, 255), (30, 150))
        self.tT.centerAt(150, 240)

        self.fT = Text("Freeplay", fontLibrary.heading, (0, 0, 0), (30, 150))
        self.fT.centerAt(150, 440)

        self.tE = Text("Examines principles related to (specifically) the American voting system, such as\nthe spoiler effect, the Electoral College, and polarization. \nAll levels are handmade, and the goal is to understand how candidates may \nposition themselves for the best chance of winning an election.",
                       fontLibrary.body, (255, 255, 255), (300, 150))

        self.fE = Text("This section is meant to apply the concepts learned in the tutorial, and you create \ncustom settings, which are then randomly applied, to see how many voting scenarios \nyou could win.",
                       fontLibrary.body, (255, 255, 255), (300, 350))

        # self.credits = Text('Coding-Frank, Art-Frank, Music-"Who Likes To Party" Kevin Macleod', fontLibrary.body, (255, 255, 255), (20, 570))

        self.back = loader.load_image("back", size=(933, 600))
        self.logo = loader.load_image("logo", size=(250, 125))
        self.gameScreen = gameScreen

    def render(self, screen):
        screen.blit(self.back, (0, 0))
        screen.blit(self.logo, (342, 25))
        screen.blit(self.tutorial, (30, 150))
        screen.blit(self.freeplay, (30, 350))

        self.tT.render(screen)
        self.fT.render(screen)
        self.tE.render(screen)
        self.fE.render(screen)
        # self.credits.render(screen)

    def tick(self, dt, mousePos, mouseClicked, prevMouseClicked):
        self.tT.centerAt(150, 240)
        self.fT.centerAt(150, 440)
        self.tE.pos = (300, 150)
        self.fE.pos = (300, 350)
        if 30 <= mousePos[0] <= 270:
            if 150 <= mousePos[1] <= 330: # tutorial
                self.tT.set_color((100, 100, 100))
                if mouseClicked and not prevMouseClicked:
                    self.screenManager.switch(1, 0.5)

            else:
                self.tT.set_color((255, 255, 255))

            if 350 <= mousePos[1] <= 530: # freeplay
                self.fT.set_color((100, 100, 100))
                if mouseClicked and not prevMouseClicked:
                    self.screenManager.switch(2, 0.5)
                    self.gameScreen.simulator = Simulator(0, settings=self.gameScreen.settings)

            else:
                self.fT.set_color((0, 0, 0))

        else:
            self.tT.set_color((255, 255, 255))
            self.fT.set_color((0, 0, 0))

    def transition01(self, screen):
        screen.blit(self.back, (0, 0))
        screen.blit(self.logo, (342-self.screenManager.time*10000, 25))

        screen.blit(self.tutorial, (30-self.screenManager.time*5000, 150))
        screen.blit(self.freeplay, (30-self.screenManager.time*5000, 350))

        self.tT.centerAt(150-5000*self.screenManager.time, 240)
        self.fT.centerAt(150-5000*self.screenManager.time, 440)
        self.tE.pos = (300-5000*self.screenManager.time, 150)
        self.fE.pos = (300-5000*self.screenManager.time, 350)

        self.tT.render(screen)
        self.fT.render(screen)
        self.tE.render(screen)
        self.fE.render(screen)

    def transition10(self, screen):
        screen.blit(self.back, (0, 0))
        screen.blit(self.logo, (self.screenManager.time*10000-4658, 25))
        screen.blit(self.tutorial, (self.screenManager.time*10000-4970, 150))
        screen.blit(self.freeplay, (self.screenManager.time*10000-4970, 350))

        self.tT.centerAt(10000*self.screenManager.time-4850, 240)
        self.fT.centerAt(10000*self.screenManager.time-4850, 440)
        self.tE.pos = (10000*self.screenManager.time-4700, 150)
        self.fE.pos = (10000*self.screenManager.time-4700, 350)

        self.tT.render(screen)
        self.fT.render(screen)
        self.tE.render(screen)
        self.fE.render(screen)
