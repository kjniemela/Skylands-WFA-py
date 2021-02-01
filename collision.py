def screen_coords(point, camX, camY):
    return (point[0]-camX, -(point[1]-camY))

#screen coord transformations
def extend_line_up(x1, y1, x2, y2, y):
    if y1 < y2:
        s = (x1-x2)/(y1-y2)
        return (x1+((y-y1)*s), y, x2, y2)
    else:
        s = (x2-x1)/(y2-y1)
        return (x1, y, x2+((y-y2)*s), y2)
    
def extend_line_down(x1, y1, x2, y2, y):
    if y1 > y2:
        s = (x1-x2)/(y2-y1)
        return (x1+((y-y1)*s), y, x2, y2)
    else:
        s = (x2-x1)/(y1-y2)
        return (x1, y, x2+((y-y2)*s), y2)

def line_collision(line1, line2):
    x1, y1, x2, y2 = line1
    x3, y3, x4, y4 = line2
    try:
        uA = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
        uB = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
    except ZeroDivisionError:
        return (False, 0, 0)
    if uA >= 0 and uA <= 1 and uB >= 0 and uB <= 1:
        intersectionX = x1 + (uA * (x2-x1))
        intersectionY = y1 + (uA * (y2-y1))
        return (True, intersectionX, intersectionY)
    else:
        return (False, 0, 0)
