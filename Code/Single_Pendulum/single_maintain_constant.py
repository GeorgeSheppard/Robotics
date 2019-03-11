import numpy as np


class MaintainConstant():
    """
    This is an example algorithm class, as everyone will be working on different algorithms
    """

    def __init__(self, values, all_data, **kwargs):
        print 'Starting maintain'
        self.start_time = values['time']
        self.max_angle = kwargs.get('max_angle', 180)
        self.duration = kwargs.get('duration', 20)

    def algo(self, values, all_data):

        if values['be'] > self.max_angle - 11.0:
            print 'Big encoder at kick command', values['be']
            return 'extended'
        if values['be'] < -self.max_angle + 11.0:
            print 'Big encoder at kick command', values['be']
            return 'seated'

        if values['time'] - self.start_time > self.duration:
            return 'switch'
