from numpy import sign

class IncreaseAngularVelocity():

    def __init__(self, values, all_data, **kwargs):
        self.start_time = values['time']
        self.max_angle = kwargs.get('max_angle', 180)
        self.increasing = kwargs.get('increasing', True)
        self.duration = kwargs.get('duration', float('inf'))
        self.min_angle = kwargs.get('min_angle', 5)
        self.previous_max_angle = all_data['be'].max()

    def algo(self, values, all_data):
        """
        Use the angular velosity to estimate the time to switch the posture
        """
        current_av = values['av']
        current_pos = values['pos']
        previous_av = all_data['av'][-1]
        print 'Time: {:.2f}'.format(values['time']), 'Big encoder value: {:.2f}'.format(values['be'])
        if(self.increasing == True):
            if(sign(current_av) != sign(previous_av)):
                self.previous_max_angle = all_data['be'][-1]
                if(current_pos == 'seated'):
                    print('extended', values['be'])
                    return 'extended'
                elif(current_pos == 'extended'):
                    print('seated', values['be'])
                    return 'seated'
            else:
                pass
        elif(self.increasing == False):
            if(sign(current_av) != sign(previous_av) and sign(previous_av) == -1):
                self.previous_max_angle = all_data['be'][-1]
                print('extended', values['be'])
                return 'extended'
            elif(sign(current_av) != sign(previous_av) and sign(previous_av) == 1):
                self.previous_max_angle = all_data['be'][-1]
                print('seated', values['be'])
                return 'seated'

        # switch conditions
        if(self.increasing == True):
            print 'Increase', values['time']
            if abs(values['be']) > self.max_angle:
                return 'switch'
        elif(self.increasing == False):
            print 'Decrease', values['time']
            if abs(self.previous_max_angle) < self.min_angle:
                return 'switch'
        if values['time'] - self.start_time > self.duration:
            return 'switch'

class DecreaseAngularVelocity(IncreaseAngularVelocity):
    def __init__(self, values, all_data, **kwargs):
        IncreaseAngularVelocity.__init__(self, values, all_data, **kwargs)
