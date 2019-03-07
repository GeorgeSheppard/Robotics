from time import time

'''My attempt to implement Georges idea for gaining amplitude.
   Instead of using the encoder angle, the total angle of NAOs 
   position to the swing is used.'''

import time as tme
import numpy as np
from utility_functions import last_maxima, last_zero_crossing, moving_average


class IncreaseQuarterPeriod():

    def __init__(self, values, all_data, **kwargs):
        # offset is time from maximum to swing
        self.time_switch = 100
        self.offset = -0.2
        self.last_maximum = self.last_maxima(all_data, 'be')

        # setting up times
        self.start_time = values['time']
        self.previous_time = values['time']
        self.previous_be = values['be']

        # max_angle used for increasing min_angle for decreasing
        self.increasing = kwargs.get('increasing', True)
        self.max_angle = kwargs.get('max_angle', 180)
        self.min_angle = kwargs.get('min_angle', 5)
        
        # alternative switch condition
        self.duration = kwargs.get('duration', float('inf'))

        if self.increasing:
            print 'Increasing amplitude, quarter period'
        else:
            print 'Decreasing amplitude, quarter period'

    def algo(self, values, all_data):

        # sign of big encoder changes when crossing zero point
        if np.sign(values['be']) != np.sign(self.previous_be):

            self.min_time = last_zero_crossing(values, self.previous_time, self.previous_be)
            self.max_time = last_maxima(all_data, be_time='time')
            # quarter period difference between time at maxima and minima
            self.quart_period = np.abs(self.min_time - self.max_time)

            # set time for position to switch
            self.time_switch = self.min_time + self.quart_period + self.offset
            self.last_maximum = last_maxima(all_data, be_time='be')
            print 'Next switching time', self.time_switch

        # At the end of the loop, set the value of big encoder to the previous value
        self.previous_be = values['be']
        self.previous_time = values['time']

        if values['time'] > self.time_switch:
            self.time_switch += 100
            return self.next_position_calculation(values)

        return self.end_conditions(values)

    def end_conditions(self, values):
        # either conditions met
        if values['time'] - self.start_time > self.duration:
            if self.increasing == True:
                print 'Switching from increasing, duration ended'
            else:
                print 'Switching from decreasing, duration ended'
            return 'switch'
        if (self.last_maximum > self.max_angle and self.increasing == True):
            print 'Maximum angle reached, switching'
            return 'switch'
        if (self.last_maximum < self.min_angle and self.increasing == False):
            print 'Minimum angle reached, switching'
            return 'switch'
        return 'no change'

    def next_position_calculation(self, values):
        if values['be'] < 0 and self.increasing == True:
            next_position = 'seated'
        elif values['be'] > 0 and self.increasing == True:
            next_position = 'extended'
        elif values['be'] < 0 and self.increasing == False:
            next_position = 'extended'
        elif values['be'] > 0 and self.increasing == False:
            next_position = 'seated'
        else:
            print "CONDITIONS DON'T CORRESPOND TO ANY POSITION, POSITION KEEPING CONSTANT"
            next_position = values['pos']
        return next_position


class DecreaseQuarterPeriod(IncreaseQuarterPeriod):
    def __init__(self, values, all_data, **kwargs):
        IncreaseQuarterPeriod.__init__(self, values, all_data, **kwargs)
