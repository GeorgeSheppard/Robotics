from utility_functions import last_maxima, last_zero_crossing
from numpy import sign

class MaintainFeedback():

    def __init__(self, values, all_data, **kwargs):
        self.start_time = values['time']
        self.previous_be = values['be']
        self.previous_time = values['time']
        self.maintain_angle = kwargs.get('maintain_angle', 10)

        # offset is time from maximum to swing
        self.time_switch = 100
        self.offset = -0.2
        self.last_maximum = last_maxima(all_data, be_time='be')

        # alternative switch condition
        self.duration = kwargs.get('duration', float('inf'))

    def algo(self, values, all_data):
        
        # sign of big encoder changes when crossing zero point
        if sign(values['be']) != sign(self.previous_be):

            self.min_time = last_zero_crossing(values, self.previous_time, self.previous_be)
            self.max_time = last_maxima(all_data, be_time='time')
            self.max_angle = last_maxima(all_data, be_time='be')

            if abs(self.max_angle) > self.maintain_angle - 0.5:
                self.offset -= 0.1
            if abs(self.max_angle) < self.maintain_angle + 0.5:
                self.offset += 0.1

            # quarter period difference between time at maxima and minima
            self.quart_period = abs(self.min_time - self.max_time)

            # set time for position to switch
            self.time_switch = self.min_time + self.quart_period + self.offset
            # Need to adjust offset based on difference between max angle and supposed maintain angle

            print 'Next switching time: {:.2f}'.format(self.time_switch), 'Last maximum: {:.2f}'.format(self.max_angle)

        # At the end of the loop, set the value of big encoder to the previous value
        self.previous_be = values['be']
        self.previous_time = values['time']

        if values['time'] > self.time_switch:
            self.time_switch += 100
            return self.next_position_calculation(values)

        if values['time'] - self.start_time > self.duration:
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
