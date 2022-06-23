from utils import *
from config import config

class Surface:
    def __init__(self, p, q):
        self.p = p
        self.q = q
        self.line = (p, q)
        self.dst = (q - p)
        self.normal = self.dst.perpendicular().normalized()

        if self.normal @ Vec(0, 1) >= 1 - math.sin(math.radians(0.25)):
            self.normal = Vec(0, 1)

        if config["debug"] and config["verbose"]:
            print("Surface(%s, dst=%s, normal=%s)" % (self.line, self.dst, self.normal))


class Platform:
    def __init__(self, texture, x, y, w, h, d, visible=True):
        self.x, self.y, self.w, self.h, self.d, self.visible = x, y, w, h, d, visible
        if visible == True:
            self.texture = texture

    def get_verts(self, camX, camY, b=1):
        x1 = self.x - ((self.w/2) * Cos(-self.d)*b) + ((self.h/2) * Sin(-self.d)*b)
        y1 = self.y + ((self.h/2) * Cos(-self.d)*b) + ((self.w/2) * Sin(-self.d)*b)
        x2 = self.x + ((self.w/2) * Cos(-self.d)*b) + ((self.h/2) * Sin(-self.d)*b)
        y2 = self.y + ((self.h/2) * Cos(-self.d)*b) - ((self.w/2) * Sin(-self.d)*b)

        x3 = self.x - ((self.w/2) * Cos(-self.d)*b) - ((self.h/2) * Sin(-self.d))
        y3 = self.y - ((self.h/2) * Cos(-self.d)*b) + ((self.w/2) * Sin(-self.d))
        x4 = self.x + ((self.w/2) * Cos(-self.d)*b) - ((self.h/2) * Sin(-self.d))
        y4 = self.y - ((self.h/2) * Cos(-self.d)*b) - ((self.w/2) * Sin(-self.d))

        return [
            (x1, y1),
            (x2, y2),
            (x3, y3),
            (x4, y4)
            ]

##        return [
##            (x1-camX, -(y1-camY)),
##            (x2-camX, -(y2-camY)),
##            (x3-camX, -(y3-camY)),
##            (x4-camX, -(y4-camY))
##            ]

    def collides_with_line(self, px1, py1, px2, py2):
        x1 = self.x-((self.w/2)*Cos(-self.d))+((self.h/2)*Sin(-self.d))
        y1 = self.y+((self.h/2)*Cos(-self.d))+((self.w/2)*Sin(-self.d))
        x2 = self.x+((self.w/2)*Cos(-self.d))+((self.h/2)*Sin(-self.d))
        y2 = self.y+((self.h/2)*Cos(-self.d))-((self.w/2)*Sin(-self.d))

        x3 = self.x-((self.w/2)*Cos(-self.d))-((self.h/2)*Sin(-self.d))
        y3 = self.y-((self.h/2)*Cos(-self.d))+((self.w/2)*Sin(-self.d))
        x4 = self.x+((self.w/2)*Cos(-self.d))-((self.h/2)*Sin(-self.d))
        y4 = self.y-((self.h/2)*Cos(-self.d))-((self.w/2)*Sin(-self.d))

##        blitRotateCenter(win, cursor, 0, (x1-8, -y1-8), (camX,camY))
##        blitRotateCenter(win, cursor, 0, (x2-8, -y2-8), (camX,camY))
##        blitRotateCenter(win, cursor, 0, (x3-8, -y3-8), (camX,camY))
##        blitRotateCenter(win, cursor, 0, (x4-8, -y4-8), (camX,camY))
##        pygame.draw.aaline(win, (111, 255, 239, 0.5), (x1-camX, -(y1-camY)), (x2-camX, -(y2-camY)))
##        pygame.draw.aaline(win, (111, 255, 239, 0.5), (x2-camX, -(y2-camY)), (x4-camX, -(y4-camY)))
##        pygame.draw.aaline(win, (111, 255, 239, 0.5), (x3-camX, -(y3-camY)), (x4-camX, -(y4-camY)))
##        pygame.draw.aaline(win, (111, 255, 239, 0.5), (x3-camX, -(y3-camY)), (x1-camX, -(y1-camY)))
        #self.d = (self.d+1)%360

        if line_collision((px1, py1, px2, py2), (x1, y1, x2, y2))[0]:
            #print(line_collision((px1, py1, px2, py2), (x1, y1, x2, y2)))
            #pygame.draw.aaline(win, (255, 0, 0, 0.5), (px1-camX, -(py1-camY)), (px2-camX, -(py2-camY)))
            return True
        elif line_collision((px1, py1, px2, py2), (x3, y3, x4, y4))[0]:
            #print(line_collision((px1, py1, px2, py2), (x3, y3, x4, y4)))
            #pygame.draw.aaline(win, (255, 0, 0, 0.5), (px1-camX, -(py1-camY)), (px2-camX, -(py2-camY)))
            return True
        elif line_collision((px1, py1, px2, py2), (x2, y2, x4, y4))[0]:
            #print(line_collision((px1, py1, px2, py2), (x2, y2, x4, y4)))
            #pygame.draw.aaline(win, (255, 0, 0, 0.5), (px1-camX, -(py1-camY)), (px2-camX, -(py2-camY)))
            return True
        elif line_collision((px1, py1, px2, py2), (x3, y3, x1, y1))[0]:
            #print(line_collision((px1, py1, px2, py2), (x3, y3, x1, y1)))
            #pygame.draw.aaline(win, (255, 0, 0, 0.5), (px1-camX, -(py1-camY)), (px2-camX, -(py2-camY)))
            return True
        else:
            #pygame.draw.aaline(win, (0, 255, 0, 0.5), (px1-camX, -(py1-camY)), (px2-camX, -(py2-camY)))
            return False
