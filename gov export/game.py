import pygame.draw

import loader
from simulator import Simulator
from text import Text


class GameScreen:
    def __init__(self, screenManager, fontLibrary):
        self.screenManager = screenManager
        self.fontLibrary = fontLibrary
        self.simulator = None
        self.back = loader.load_image("back", size=(933, 600))

        self.text = Text("Simulator", fontLibrary.heading, (255, 255, 255), (30, 10))
        self.exit = loader.load_image("exit")

        self.settings = {"num_spaces":1, "num_candidates":2, "space_1":{"numvoters":100, "clusters":0, "polar":0},
                         "space_2":{"numvoters":100, "clusters":0, "polar":0}, "space_3":{"numvoters":100, "clusters":0, "polar":0}}
        self.generated = True

    def generate(self):
        self.simulator = Simulator(0, settings=self.settings)
        self.generated = True


    def render(self, screen):
        colors = {
            -1:(128, 128, 128),
            0:(227, 76, 76),
            1:(76, 172, 227),
            2:(255, 255, 97)
        }
        screen.blit(self.back, (0, 0))
        self.text.render(screen)
        screen.blit(self.exit, (800, 50))
        self.simulator.draw(screen)

        overall = [0 for i in range(len(self.simulator.spaces[0].candidates))]
        for space in self.simulator.spaces:
            eval = space.evaluate()
            maxindex = 0
            for index, i in enumerate(eval):
                if i > eval[maxindex]:
                    maxindex = index

            overall[maxindex] += 1

        overall = [i/sum(overall) for i in overall]
        x = 0
        for index, i in enumerate(overall):
            pygame.draw.rect(screen, colors[index], pygame.Rect(x+600, 500, 300*i, 50))
            x += 300*i

        if self.simulator.level > 0:
            with open(f"assets/descs/{self.simulator.level}.txt") as f:
                text = f.read()

            Text(text, self.fontLibrary.body, (255, 255, 255), (600, 150)).render(screen)

        else:
            Text("Click the rectangles to\ntoggle any of these \nsettings", self.fontLibrary.body, (255, 255, 255), (600, 60)).render(screen)
            Text("# Candidates", self.fontLibrary.body, (255, 255, 255), (600, 150)).render(screen)
            Text("# Voting Spaces", self.fontLibrary.body, (255, 255, 255), (600, 190)).render(screen)

            Text("1", self.fontLibrary.body, (255, 255, 255), (600, 250)).render(screen)
            if self.settings["num_spaces"] >= 2:
                Text("2", self.fontLibrary.body, (255, 255, 255), (600, 290)).render(screen)

            if self.settings["num_spaces"] >= 3:
                Text("3", self.fontLibrary.body, (255, 255, 255), (600, 330)).render(screen)

            Text("Space", self.fontLibrary.body, (255, 255, 255), (600, 220)).render(screen)
            Text("Clusters", self.fontLibrary.body, (255, 255, 255), (660, 220)).render(screen)
            Text("# Voters", self.fontLibrary.body, (255, 255, 255), (750, 220)).render(screen)
            Text("Polarity", self.fontLibrary.body, (255, 255, 255), (840, 220)).render(screen)

            pygame.draw.rect(screen, (0, 69, 3), pygame.Rect(750, 150, 50, 24))
            pygame.draw.rect(screen, (0, 69, 3), pygame.Rect(750, 190, 50, 24))

            for x in [660, 750, 840]:
                for index, y in enumerate([250, 290, 330]):
                    if index < self.settings["num_spaces"]:
                        pygame.draw.rect(screen, (0, 69, 3), pygame.Rect(x, y, 50, 24))

            t = Text(str(self.settings["num_candidates"]), self.fontLibrary.body, (255, 0, 0), (0, 0))
            t.centerAt(775, 162)
            t.render(screen)

            t = Text(str(self.settings["num_spaces"]), self.fontLibrary.body, (255, 0, 0), (0, 0))
            t.centerAt(775, 202)
            t.render(screen)

            for index, y in enumerate([250, 290, 330]):
                if index < self.settings["num_spaces"]:
                    t = Text(str(self.settings[f"space_{index+1}"]["clusters"]), self.fontLibrary.body, (255, 0, 0), (0, 0))
                    t.centerAt(685, y+12)
                    t.render(screen)

                    t = Text(str(self.settings[f"space_{index+1}"]["numvoters"]), self.fontLibrary.body, (255, 0, 0), (0, 0))
                    t.centerAt(775, y+12)
                    t.render(screen)

                    polarity = ""
                    if self.settings[f"space_{index+1}"]["polar"] == 0:
                        polarity = "None"

                    elif self.settings[f"space_{index+1}"]["polar"] == 1:
                        polarity = "Some"

                    else:
                        polarity = "Lots"

                    t = Text(polarity, self.fontLibrary.body, (255, 0, 0), (0, 0))
                    t.centerAt(865, y+12)
                    t.render(screen)

        if len(self.simulator.spaces) > 1:
            Text("Electoral College", self.fontLibrary.heading, (0, 0, 0), (610, 490)).render(screen)
            overall = [0 for i in range(len(self.simulator.spaces[0].candidates))]
            for space in self.simulator.spaces:
                space.evaluate()
                for i in space.preference:
                    overall[i] += 1


            overall = [i/sum(overall) for i in overall]
            x = 0
            for index, i in enumerate(overall):
                pygame.draw.rect(screen, colors[index], pygame.Rect(x+600, 400, 300*i, 50))
                x += 300*i

            Text("Popular Vote", self.fontLibrary.heading, (0, 0, 0), (610, 390)).render(screen)



    def tick(self, dt, mousePos, mouseClicked, prevMouseClicked):
        if not self.generated:
            self.generate()

        self.text.pos = (30, 10)
        if 800 <= mousePos[0] <= 880 and 50 <= mousePos[1] <= 130:
            if mouseClicked and not prevMouseClicked:
                self.screenManager.switch(0, 0.5)

        self.simulator.tick(dt, mousePos, mouseClicked, prevMouseClicked)

        if not prevMouseClicked and mouseClicked:
            if pygame.Rect(750, 150, 50, 24).collidepoint(*mousePos):
                self.settings["num_candidates"] = 5-self.settings["num_candidates"]
                self.generated = False

            if pygame.Rect(750, 190, 50, 24).collidepoint(*mousePos):
                self.settings["num_spaces"] %= 3
                self.settings["num_spaces"] += 1
                self.generated = False

            for x in [660, 750, 840]:
                for index, y in enumerate([250, 290, 330]):
                    if index < self.settings["num_spaces"]:
                        if pygame.Rect(x, y, 50, 24).collidepoint(*mousePos):
                            edit = self.settings[f"space_{index+1}"]
                            if x == 750:
                                edit["numvoters"] %= 200
                                edit["numvoters"] += 50
                                self.generated = False

                            elif x == 660:
                                edit["clusters"] += 1
                                edit["clusters"] %= 5
                                self.generated = False

                            else:
                                edit["polar"] += 1
                                edit["polar"] %= 3
                                self.generated = False


    def transitionIn(self, screen):
        screen.blit(self.back, (0, 0))
        self.text.pos = (5000*self.screenManager.time-(2500-30), 10)
        self.text.render(screen)
        screen.blit(self.exit, (-5000*self.screenManager.time+3300, 50))

    def transitionOut(self, screen):
        self.text.pos = (-5000*self.screenManager.time+30, 10)
        self.text.render(screen)
        screen.blit(self.exit, (5000*self.screenManager.time+800, 50))
