from time import time

class Start():
    def __init__(self, values, **kwargs):
        self.start_time = time()
        self.duration = kwargs.get('duration', 5)

        pass
    
    def algo(self, values):
        print 'start', values['time']
        if time() - self.start_time > self.duration:
            return 'switch'