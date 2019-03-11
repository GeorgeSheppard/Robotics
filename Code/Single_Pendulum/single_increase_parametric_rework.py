from numpy import sign
from utility_functions import last_maxima, last_zero_crossing


class IncreaseParametric():

    def __init__(self, values, all_data, **kwargs):
        """
        Set up the parameters for parametric pumping.
        """
        self.start_time = values['time']
        self.increasing = kwargs.get('increasing', True)

        # conditions for finishing
        self.max_angle = kwargs.get('max_angle', float('inf'))
        self.duration = kwargs.get('duration', float("inf"))

        # previous values
        self.prev_be = values['be']
        self.prev_time = values['time']

        # time to swing from min and maximum
        self.min_offset = -0.35
        self.max_offset = -0.35

        # stop immediate trigger of swing
        self.next_max = self.start_time + 100
        self.next_min = self.start_time + 100

    def algo(self, values, all_data, **kwargs):
        print values['time'], values['be']

        if sign(values['be']) != sign(self.prev_be):

            # calculate true zero crossing point
            true_zero_time = last_zero_crossing(values, self.prev_time, self.prev_be)

            # calculate quarter period based on latest maximum and minimum
<<<<<<< HEAD
            self.max_times = last_maxima(all_data['time'], all_data['be'], be_time='time')
            quarter_period = abs(self.max_times[-1] - true_zero_time)
=======
            self.max_times = last_maxima(all_data, be_time='time')
            quarter_period = abs(self.max_times - true_zero_time)
>>>>>>> master

            # maximum and minimum point
            self.next_max = true_zero_time + quarter_period + self.max_offset
            self.next_min = true_zero_time + 2 * quarter_period + self.min_offset
            print values['time'], self.next_max, self.next_min

        self.prev_be = values['be']
        self.prev_time = values['time']

        # if time to switch change to correct position
        if values['time'] > self.next_max:
            self.next_max += 100
            if self.increasing:
                return 'lowered'
            else:
                return 'raised'
        if values['time'] > self.next_min:
            self.next_min += 100
            if self.increasing:
                return 'raised'
            else:
                return 'lowered'

        # switch if angle is big enough or duration is over
        if values['time'] - self.start_time > self.duration:
            print 'Duration end', values['time'], self.start_time, self.duration
            return 'switch'
        if values['be'] > self.max_angle:
            print 'Angle end', values['be'], self.max_angle
            return 'switch'

class DecreaseParametric(IncreaseParametric):
    def __init__(self, values, all_data, **kwargs):
        IncreaseParametric.__init__(self, values, all_data, **kwargs)
