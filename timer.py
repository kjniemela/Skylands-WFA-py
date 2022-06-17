from time import time

class TimerController:
    def __init__(self):
        self.timers = []
        self.events = []

    def set_timeout(self, fn, interval):
        end_time = time() + (interval / 1000)
        i = 0
        while i < len(self.timers) and end_time >= self.timers[i][0]:
            i += 1
        self.timers.insert(i, (end_time, fn))

    def set_condition(self, fn, condition):
        self.events.append((condition, fn))

    def check_all(self):
        i = 0
        while i < len(self.timers):
            timer = self.timers[i]
            if time() > timer[0]:
                timer[1]()
                del self.timers[i]
            else:
                break
            i += 1

        i = 0
        while i < len(self.events):
            event = self.events[i]
            if event[0]():
                event[1]()
                del self.events[i]
            i += 1
            
timers = TimerController()