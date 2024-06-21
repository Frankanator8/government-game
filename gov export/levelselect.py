import loader
from simulator import Simulator
from text import Text


class LevelSelect:
    def __init__(self, screenManager, fontLibrary, gameScreen):
        self.screenManager = screenManager
        self.fontLibrary = fontLibrary
        self.gameScreen = gameScreen

        self.text = Text("Level Select", self.fontLibrary.heading, (255, 255, 255), (30, 30))
        self.back = loader.load_image("back", size=(933, 600))
        self.coalition = loader.load_image("coalition")
        self.polar = loader.load_image("polar")
        self.spoiler = loader.load_image("spoiler")
        self.wta = loader.load_image("winnertakesall")
        self.electoral = loader.load_image("electoral")

        self.exit = loader.load_image("exit")

    def transition01(self, screen):
        self.text.pos = (5000*self.screenManager.time-(2500-30), 30)
        self.text.render(screen)

        screen.blit(self.coalition, (5000*self.screenManager.time-(2500-30), 150))
        screen.blit(self.polar, (5000*self.screenManager.time-(2500-260), 150))
        screen.blit(self.spoiler, (5000*self.screenManager.time-(2500-30), 300))
        screen.blit(self.wta, (5000*self.screenManager.time-(2500-260), 300))
        screen.blit(self.electoral, (5000*self.screenManager.time-(2500-30), 450))

        screen.blit(self.exit, (-5000*self.screenManager.time+3300, 50))

    def transition10(self, screen):
        self.text.pos = (-5000*self.screenManager.time+30, 30)
        self.text.render(screen)

        screen.blit(self.coalition, (-5000*self.screenManager.time-(-30), 150))
        screen.blit(self.polar, (-5000*self.screenManager.time-(-260), 150))
        screen.blit(self.spoiler, (-5000*self.screenManager.time-(-30), 300))
        screen.blit(self.wta, (-5000*self.screenManager.time-(-260), 300))
        screen.blit(self.electoral, (-5000*self.screenManager.time-(-30), 450))

        screen.blit(self.exit, (5000*self.screenManager.time+800, 50))

    def render(self, screen):
        screen.blit(self.back, (0, 0))
        self.text.render(screen)

        screen.blit(self.coalition, (30, 150))
        screen.blit(self.polar, (260, 150))
        screen.blit(self.spoiler, (30, 300))
        screen.blit(self.wta, (260, 300))
        screen.blit(self.electoral, (30, 450))

        screen.blit(self.exit, (800, 50))

    def tick(self, dt, mousePos, mouseClicked, prevMouseClicked):
        self.text.pos = (30, 30)
        if 800 <= mousePos[0] <= 880 and 50 <= mousePos[1] <= 130:
            if mouseClicked and not prevMouseClicked:
                self.screenManager.switch(0, 0.5)

        if mouseClicked and not prevMouseClicked:
            if 30 <= mousePos[0] <= 230:
                if 150 <= mousePos[1] <= 250:
                    self.gameScreen.simulator = Simulator(1)
                    self.screenManager.switch(2, 0.5)

                elif 300 <= mousePos[1] <= 400:
                    self.gameScreen.simulator = Simulator(3)
                    self.screenManager.switch(2, 0.5)

                elif 450 <= mousePos[1] <= 550:
                    self.gameScreen.simulator = Simulator(5)
                    self.screenManager.switch(2, 0.5)

            elif 260 <= mousePos[0] <= 460:
                if 150 <= mousePos[1] <= 250:
                    self.gameScreen.simulator = Simulator(2)
                    self.screenManager.switch(2, 0.5)

                elif 300 <= mousePos[1] <= 400:
                    self.gameScreen.simulator = Simulator(4)
                    self.screenManager.switch(2, 0.5)



