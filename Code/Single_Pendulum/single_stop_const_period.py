'''Stop algorithm that simply kicks, waits a half period,
    and kicks again. Calculates correct kicking order as will already be in 
    motion, and times starting kick to next maxima.'''


from utility_functions import last_maxima

class Stop():
    def __init__(self, values, all_data, **kwargs):
        self.start_time = values['time']
        self.duration = kwargs.get('duration', float('inf'))
        self.min_angle = kwargs.get('min_angle', 1.0)
        self.wait_time = 1.25
        self.last_move = last_maxima(all_data['time'], all_data['be'], 'time')

        # sets up correct position
        av = values['av']
        if av >= 0:
            # positive angular momentum means going backward, therefore want seated to decrease
            self.start_pos = 'seated'
        else:
            # opposite of above
            self.start_pos = 'extended'
        print 'Stopping swing, constant period'

    def algo(self, values, all_data):
        t = values['time']

        if t > self.last_move + self.wait_time:
            print 'Stop swing', values['time']
            self.last_move = t
            return self.next_position(values)

        # ending if duration is over or minimum angle is reached
        if t - self.start_time > self.duration:
            print 'duration reached, stopping'
            return 'switch'
        if last_maxima(all_data['time'], all_data['be'], 'be') < self.min_angle:
            print 'min angle reached, stopping'
            return 'switch'

    def next_position(self, values):
        if values['pos'] == 'seated':
            return 'extended'
        else:
            return 'seated'
