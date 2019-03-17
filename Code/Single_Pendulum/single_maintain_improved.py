import numpy as np
from utility_functions import last_maxima, last_zero_crossing, moving_average, sign_zero


class MaintainGoodBadKick():
    """
    This is an example algorithm class, as everyone will be working on different algorithms
    """

    def __init__(self, values, all_data, **kwargs):
        self.period = kwargs.get('period', 0.005)
        # offset is time from maximum to swing
        self.time_switch = 100
        self.offset = -0.1
        self.last_maximum = last_maxima(all_data['time'], all_data['be'], time_values='values', dt=self.period)

        # setting up times
        self.start_time = values['time']
        self.previous_time = values['time']
        self.previous_be = values['be']

        self.maintain_angle = kwargs.get('maintain_angle', 10.0)

        # alternative switch condition
        self.duration = kwargs.get('duration', float('inf'))

        self.offsets = {
            'good': -0.25,
            'poor': -0.5,
            'standard': 0.0
        }

    def algo(self, values, all_data):

        # sign of big encoder changes when crossing zero point
        if sign_zero(values['be']) != sign_zero(self.previous_be):
            self.min_time = last_zero_crossing(values, self.previous_time, self.previous_be)
            self.max_time, self.last_maximum = last_maxima(all_data['time'], all_data['be'], time_values='both', dt=self.period)
            # quarter period difference between time at maxima and minima
            self.quart_period = np.abs(self.min_time - self.max_time)

            # if at amplitude it's meant to be at then standard offset
            print 'Values', abs(self.last_maximum), abs(self.maintain_angle)
            if -0.2 <= abs(self.last_maximum) - abs(self.maintain_angle) <= 0.2:
                self.offset = self.offsets['standard']
            elif abs(self.last_maximum) - abs(self.maintain_angle) > 0.2:
                self.offset = self.offsets['poor']
            elif abs(self.last_maximum) - abs(self.maintain_angle) < -0.2:
                self.offset = self.offsets['good']
            else:
                print 'Offset condition not found\nLast maximum: {}, Maintain angle: {}, \
                    Difference between{}'.format(self.last_maximum, self.maintain_angle, abs(self.last_maximum) - abs(self.maintain_angle))

            # set time for position to switch
            self.time_switch = self.min_time + self.quart_period + self.offset
            print 'Current time: {:.3f}'.format(values['time']), 'Next switching time: {:.3f}'.format(self.time_switch), 'Last maximum: {:.3f}'.format(self.last_maximum)

        # At the end of the loop, set the value of big encoder to the previous value
        self.previous_be = values['be']
        self.previous_time = values['time']

        if values['time'] > self.time_switch:
            self.time_switch += 100
            return self.next_position_calculation(values)

        if values['time'] - self.start_time > self.duration:
            print 'Switching from maintaining, duration ended'
            return 'switch'


    def next_position_calculation(self, values):
        if values['be'] < 0:
            next_position = 'seated'
        elif values['be'] > 0:
            next_position = 'extended'
        else:
            print "CONDITIONS DON'T CORRESPOND TO ANY POSITION, POSITION KEEPING CONSTANT"
            next_position = values['pos']
        return next_position