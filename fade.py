class Fade:
    def __init__(self, fadeWhite, fadeBlack):
        self.fadeWhite = fadeWhite
        self.fadeBlack = fadeBlack
        self.alpha = 0
        self.active = False
        self.color = "black"
        self.speed = 1
        self.on_complete = None
        self.fading = True
    def fade_white(self, speed, on_complete):
        self.color = "white"
        self.speed = speed
        self.on_complete = on_complete
        self.active = True
        self.fading = True
    def fade_black(self, speed, on_complete):
        self.color = "black"
        self.speed = speed
        self.on_complete = on_complete
        self.active = True
        self.fading = True
    def draw_static(self, win, alpha):
        if self.color == "white":
            self.fadeWhite.set_alpha(alpha)
            win.blit(self.fadeWhite, (0,0))
        elif self.color == "black":
            self.fadeBlack.set_alpha(alpha)
            win.blit(self.fadeBlack, (0,0))
    def draw(self, win):
        global gameState
        
        if self.active:
            if self.color == "white":
                self.fadeWhite.set_alpha(self.alpha)
                win.blit(self.fadeWhite, (0,0))
            elif self.color == "black":
                self.fadeBlack.set_alpha(self.alpha)
                win.blit(self.fadeBlack, (0,0))
            if self.fading:
                if self.alpha < 255:
                    self.alpha += self.speed
                else:
                    self.fading = False
                    if self.on_complete != None:
                        self.on_complete()
            else:
                if self.alpha > 0:
                    self.alpha -= self.speed
                else:
                    self.active = False