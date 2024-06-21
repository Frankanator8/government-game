class ScreenManager:
    def __init__(self):
        self.screen = 0
        self.transition = (0, 0)
        self.transitioning = False
        self.time = 0
        self.transTime = 0

    def switch(self, screen, time):
        self.transitioning = True
        self.transition = (self.screen, screen)
        self.time = 0
        self.transTime = time

    def tick(self, dt):
        if self.transitioning:
            self.time += dt
            if self.time > self.transTime:
                self.transitioning = False
                self.screen = self.transition[1]
