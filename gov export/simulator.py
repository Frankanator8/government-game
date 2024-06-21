import math
import random

import pygame

import loader
from text import Text


class VotingSpace:
    def __init__(self):
        self.voters = []
        self.candidates = []
        self.preference = []
        self.highlight = 0

    def generate_random_map(self, numvoters=100, numcandidates=2, clusters=0, polar=0):
        if polar == 0:
            dist = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]

        elif polar == 1:
            dist = [0.15, 0.1, 0.1, 0.1, 0.05, 0.05, 0.1, 0.1, 0.1, 0.15]

        elif polar == 2:
            dist = [0.3, 0.1, 0.05, 0.05, 0, 0, 0.05, 0.05, 0.1, 0.3]

        picks = [0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95]

        votersLeft = numvoters

        if clusters > 0:
            clustersize = round(numvoters * 0.6 / clusters)
            for i in range(clusters):
                thissize = math.floor(clustersize + random.uniform(-0.4/clusters, 0.4/clusters) * numvoters)
                centerX = random.choices(picks, dist)[0] + random.uniform(-0.05, 0.05)
                centerY = random.choices(picks, dist)[0] + random.uniform(-0.05, 0.05)
                votersLeft -= thissize
                for j in range(thissize):
                    distance = random.uniform(0, 0.05)
                    angle = random.uniform(0, 2*math.pi)

                    x = centerX + distance * math.cos(angle)
                    y = centerY + distance * math.sin(angle)
                    x = min(max(x, 0), 1)
                    y = min(max(y, 0), 1)
                    self.voters.append((x, y))

        for i in range(votersLeft):
            x = random.choices(picks, dist)[0] + random.uniform(-0.05, 0.05)
            y = random.choices(picks, dist)[0] + random.uniform(-0.05, 0.05)
            x = min(max(x, 0), 1)
            y = min(max(y, 0), 1)
            self.voters.append((x, y))

        for i in range(numcandidates):
            x = random.choices(picks, dist)[0] + random.uniform(-0.05, 0.05)
            y = random.choices(picks, dist)[0] + random.uniform(-0.05, 0.05)
            x = min(max(x, 0), 1)
            y = min(max(y, 0), 1)
            self.candidates.append((x, y))

        self.preference = [-1 for i in range(len(self.voters))]
        return self

    def read_map(self, file):
        im = pygame.PixelArray(loader.load_image(file))
        for i in range(im.shape[0]):
            for j in range(im.shape[1]):
                color = im[i][j]
                r = color & 255
                g = (color >> 8) & 255
                b = (color >> 16) & 255
                if (r, g, b) == (0, 0, 0):
                    self.voters.append((i/30, j/30))

                elif (r, g, b) == (255, 255, 255):
                    pass

                else:
                    self.candidates.append((i/30, j/30))

        self.candidates.append((0.5, 0.5))

        self.preference = [-1 for i in range(len(self.voters))]
        return self

    def evaluate(self):
        voteDist = [0 for i in range(len(self.candidates))]
        for index, voter in enumerate(self.voters):
            lowestdist = 100000
            lowestindex = -1
            for indexC, candidate in enumerate(self.candidates):
                if ((candidate[0]-voter[0])**2+(candidate[1]-voter[1])**2)**(1/2) < lowestdist:
                    lowestdist = ((candidate[0]-voter[0])**2+(candidate[1]-voter[1])**2)**(1/2)
                    lowestindex = indexC

            voteDist[lowestindex] += 1
            self.preference[index] = lowestindex

        return [i/sum(voteDist) for i in voteDist]




    def draw(self, surface):

        colors = {
            -1:(128, 128, 128),
            0:(227, 76, 76),
            1:(76, 172, 227),
            2:(255, 255, 97)
        }
        pygame.draw.rect(surface, (255, 255, 255), pygame.Rect(10, 10, surface.get_width()-20, surface.get_height()-20))
        x = 0
        evalu = self.evaluate()
        for index, candidate in enumerate(self.candidates):
            pygame.draw.circle(surface, colors[index], (10+candidate[0]*(surface.get_width()-20), 10+candidate[1]*(surface.get_height()-20)), 10)
            if index == self.highlight:
                pygame.draw.circle(surface, (255, 166, 0), (10+candidate[0]*(surface.get_width()-20), 10+candidate[1]*(surface.get_height()-20)), 5)
            pygame.draw.rect(surface, colors[index], pygame.Rect(x, 0, evalu[index]*surface.get_width(), 10))
            x+=evalu[index]*surface.get_width()


        for index, candidate in enumerate(self.voters):
            pygame.draw.circle(surface, colors[self.preference[index]], (10+candidate[0]*(surface.get_width()-20), 10+candidate[1]*(surface.get_height()-20)), 5)


        return surface



class Simulator:
    def __init__(self, level, settings=None):
        self.level = level
        self.spaces = []
        if self.level == 0:
            for i in range(settings["num_spaces"]):
                if settings[f"space_{i+1}"] != {}:
                    self.spaces.append(VotingSpace().generate_random_map(numcandidates=settings["num_candidates"], **settings[f"space_{i+1}"]))

        elif self.level == 1:
            self.spaces = [VotingSpace().read_map("coalitionmap")]

        elif self.level == 2:
            self.spaces = [VotingSpace().read_map("polarmap")]

        elif self.level == 3:
            self.spaces = [VotingSpace().read_map("spoilermap")]

        elif self.level == 4:
            self.spaces = [VotingSpace().read_map("wta")]

        else:
            self.spaces = [VotingSpace().read_map("ecmap"), VotingSpace().read_map("ecmap"),
                           VotingSpace().read_map("ec2map")]

        self.results = [[] for _ in range(len(self.spaces))]
        self.mouseActive = False

    def update(self, candidateIndex, x, y):
        self.results = []
        for space in self.spaces:
            space.candidates[candidateIndex] = (x, y)
            self.results.append(space.evaluate())

    def tick(self, dt, mousePos, mouseClicked, prevMouseClicked):
        for space in self.spaces:
            space.highlight = len(space.candidates)-1

        for i in range(len(space.candidates)-1):
            self.update(i, *self.spaces[0].candidates[i])

        if len(self.results) == 1:
            if 30 <= mousePos[0] <= 530 and 60 <= mousePos[1] <= 560:
                if self.mouseActive:
                    x = (mousePos[0]-30)/500
                    y = (mousePos[1]-60)/500
                    self.update(-1, x, y)
                    if mouseClicked and not prevMouseClicked:
                        self.mouseActive = False

                else:
                    if mouseClicked and not prevMouseClicked:
                        self.mouseActive = True

        elif len(self.results)==2:
            if 30 <= mousePos[0] <= 280 and 60 <= mousePos[1] <= 280:
                if self.mouseActive:
                    x = (mousePos[0]-30)/250
                    y = (mousePos[1]-60)/250
                    self.update(-1, x, y)
                    if mouseClicked and not prevMouseClicked:
                        self.mouseActive = False

                else:
                    if mouseClicked and not prevMouseClicked:
                        self.mouseActive = True

            if 300 <= mousePos[0] <= 550 and 330 <= mousePos[1] <= 580:
                if self.mouseActive:
                    x = (mousePos[0]-300)/250
                    y = (mousePos[1]-330)/250
                    self.update(-1, x, y)
                    if mouseClicked and not prevMouseClicked:
                        self.mouseActive = False

                else:
                    if mouseClicked and not prevMouseClicked:
                        self.mouseActive = True

        else:
            if 30 <= mousePos[0] <= 280 and 60 <= mousePos[1] <= 310:
                if self.mouseActive:
                    x = (mousePos[0]-30)/250
                    y = (mousePos[1]-60)/250
                    self.update(-1, x, y)
                    if mouseClicked and not prevMouseClicked:
                        self.mouseActive = False

                else:
                    if mouseClicked and not prevMouseClicked:
                        self.mouseActive = True

            if 300 <= mousePos[0] <= 550 and 60 <= mousePos[1] <= 310:
                if self.mouseActive:
                    x = (mousePos[0]-300)/250
                    y = (mousePos[1]-60)/250
                    self.update(-1, x, y)
                    if mouseClicked and not prevMouseClicked:
                        self.mouseActive = False

                else:
                    if mouseClicked and not prevMouseClicked:
                        self.mouseActive = True

            if 175 <= mousePos[0] <= 175+250 and 330 <= mousePos[1] <= 580:
                if self.mouseActive:
                    x = (mousePos[0]-175)/250
                    y = (mousePos[1]-330)/250
                    self.update(-1, x, y)
                    if mouseClicked and not prevMouseClicked:
                        self.mouseActive = False

                else:
                    if mouseClicked and not prevMouseClicked:
                        self.mouseActive = True


        if self.level == 2:
            if self.spaces[0].candidates[-1][1] > self.spaces[0].candidates[-1][0]+0.1:
               self.update(-1, self.spaces[0].candidates[-1][0], self.spaces[0].candidates[-1][0]+0.1)

        elif self.level == 3:
            if self.spaces[0].candidates[-1][1] > self.spaces[0].candidates[-1][0]:
               self.update(-1, self.spaces[0].candidates[-1][0], self.spaces[0].candidates[-1][0])


        elif self.level == 5:
            if self.spaces[0].candidates[-1][0] < 0.7:
                self.update(-1, 0.7, self.spaces[0].candidates[-1][1])



    def draw(self, screen):
        if len(self.results) == 1:
            screen.blit(self.spaces[0].draw(pygame.Surface((500, 500))), (30, 60))

        elif len(self.results)==2:
            screen.blit(self.spaces[0].draw(pygame.Surface((250, 250))), (30, 60))
            screen.blit(self.spaces[1].draw(pygame.Surface((250, 250))), (300, 330))

        else:
            screen.blit(self.spaces[0].draw(pygame.Surface((250, 250))), (30, 60))
            screen.blit(self.spaces[1].draw(pygame.Surface((250, 250))), (300, 60))
            screen.blit(self.spaces[2].draw(pygame.Surface((250, 250))), (175, 330))
