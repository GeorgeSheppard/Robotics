import numpy as np
import math


class IncreaseDecrease():

    def __init__(self, values, all_data, **kwargs):
        print 'Starting'
        self.start_time = values['time']
        self.max_angle = kwargs.get('max_angle', 180)
        self.increase = kwargs.get('increase', True)
        self.duration = kwargs.get('duration', float('inf'))
        self.pendulum_length = 1.82
        self.min_angle = kwargs.get('min_angle', 5)
        self.next_highest_angle = None
        self.previous_max_angle = all_data['be'].max()

    def algo(self, values, all_data):
        """
        Use the max_angle approximation to estimate the time to switch the position
        """
        current_be = values['be']
        previous_be = all_data['be'][-1]
        current_av = values['av']
        previous_av = all_data['av'][-1]

        # Check if the sign of the big encoder data has changed
        # If not changed, we know the swing is not at its lowest point
        if (np.sign(previous_be) == np.sign(current_be)):
            pass
        # If the sign changed, calculate the approximation of the highest point it can reach
        else:
            self.max_speed = math.radians(values['av']) * self.pendulum_length
            h = 0.5*(self.max_speed**2)/9.8
            # Calculate the next highest angle in degrees,
            # The -2 degree at end is because we want to start change the position a little bit early
            self.next_highest_angle = math.degrees(
                math.acos((self.pendulum_length-h)/self.pendulum_length))-2
            self.next_highest_angle = np.sign(
                current_be) * self.next_highest_angle
            print values['time'], 'At lowest point', 'Big encoder {:.2f}'.format(values['be']) 

        if (self.next_highest_angle):
            next_pos = None

            if(np.sign(self.next_highest_angle) < 0 and current_be < self.next_highest_angle):
                if(self.increase == True):
                    next_pos = 'seated'
                else:
                    next_pos = 'extended'
            elif(np.sign(self.next_highest_angle) > 0 and current_be > self.next_highest_angle):
                if(self.increase == True):
                    next_pos = 'extended'
                else:
                    next_pos = 'seated'

            if(next_pos):
                self.next_highest_angle = None
                return next_pos

        if(np.sign(current_av) != np.sign(previous_av) and np.sign(previous_av) == -1):
            self.previous_max_angle = all_data['be'][-1]
            if(self.max_angle < abs(self.previous_max_angle) and self.increase == True):
                return 'switch'
            elif(abs(self.previous_max_angle) < self.min_angle and self.increase == False):
                return 'switch'
        if values['time'] - self.start_time > self.duration:
            return 'switch'
