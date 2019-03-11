import numpy as np
from numpy import sign
from utility_functions import last_maxima, last_zero_crossing, moving_average, next_position_calculation, last_minima


class Increase():

    def __init__(self, values, all_data, **kwargs):
        """
        Set up the parameters for parametric pumping.
        """
        self.start_time = values['time']
        self.max_angle = kwargs.get('max_angle', 180)
        self.increase = kwargs.get('increase', True)
        self.duration = kwargs.get('duration', float("inf"))
        self.decrease = kwargs.get('decrease', False)
        # Set decrease as True to swap raised/lowered, such that the
        # amplitude decreases, slowing down the swing (hopefully).

        if self.decrease:
            self.zero_pos = "lowered"
            self.maxima_pos = "raised"

        elif not self.decrease:
            self.zero_pos = "raised"
            self.maxima_pos = "lowered"

        self.prev, self.curr = 0.0, values['be']
        self.prev_time, self.curr_time = 0.0, values['time']
        self.moving_down = True

        self.max_times = self.last_maxima(all_data)
        self.min_times = self.last_minima(all_data)

        self.time_to_switch_unfolded = 100
        self.time_to_switch_folded = 100
        self.max_angle_reached = False

        self.tolerance_zero = -1.0
        self.tolerance_max = -0.0

    def last_maxima(self, all_data):
        """
        Obtain the time of the last maxima, on either side of the swing.
        """
        be = np.abs(all_data['be'][-30:])
        time = all_data['time'][-30:]

        # Obtain index.
        angle_max_index = (np.diff(np.sign(np.diff(be))) < 0).nonzero()[0] + 1
        max_times = time[angle_max_index]

        return max_times

    def last_minima(self, all_data):
        """
        Obtain the time at which the swing was last at the bottom of its arc.
        """
        be = np.abs(all_data['be'][-30:])
        time = all_data['time'][-30:]

        # Obtain index.
        angle_max_index = (np.diff(np.sign(np.diff(be))) > 0).nonzero()[0] + 1
        min_times = time[angle_max_index]
        return min_times

    def algo(self, values, all_data, **kwargs):
        """
        Define parametric swinging function, for current swing state 'values' and past states 'all_data'.
        See interface.py for details.
        """

        # Getting period:

        # Shuffle values around, such that we compare the current state to
        # the previous state.

        if abs(values['be']) >= self.max_angle:
            self.max_angle_reached = True  # Switch at next zero.

        self.prev, self.curr = self.curr, values['be']
        self.prev_time, self.curr_time = self.curr_time, values['time']

        if sign(self.curr) != sign(self.prev):  # Zero crossed
            print values['time'], 'Crossed zero point'
            self.moving_down = False
            self.max_times = self.last_maxima(all_data)

            dt = self.curr_time - self.prev_time
            interpolate = dt * np.abs(self.curr) / \
                np.abs(self.curr - self.prev)
            true_zero_time = values['time'] - interpolate
            quarter_period = abs(self.max_times[-1] - true_zero_time)
            self.time_to_switch_unfolded = true_zero_time + quarter_period

        # Top of swing reached.
        elif abs(self.curr) <= abs(self.prev) and not self.moving_down:
            print values['time'], 'At maximum'
            self.moving_down = True
            # Moving down flag prevents max_times from being appended to more than once.

            self.zero_times = last_minima(all_data)
            self.max_times = last_maxima(all_data)
            quarter_period = abs(self.max_times[-1] - self.zero_times[-1])
            self.time_to_switch_folded = self.max_times[-1] + quarter_period

        if values['time'] > self.time_to_switch_unfolded + self.tolerance_zero:
            self.time_to_switch_unfolded += 100  # Some arbitrary big number.
            print 'Angle', values['time'], values['be']
            return self.maxima_pos  # Change position.

        if values['time'] > self.time_to_switch_folded + self.tolerance_max:

            if values['time'] >= self.duration + self.start_time or self.max_angle_reached:
                print("Maximum duration/angle reached, switching.")
                return "switch"  # Switch ready for next zero.
            print 'Angle', values['time'], values['be']
            self.time_to_switch_folded += 100  # Some arbitrary big number.
            return self.zero_pos  # Change position.
