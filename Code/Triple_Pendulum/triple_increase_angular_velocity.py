from utility_functions import sign_zero, total_angle

class TripleIncreaseAngularVelocity():

    def __init__(self, values, all_data, **kwargs):
        self.start_time = values['time']
        self.max_angle = kwargs.get('max_angle', 180)
        self.increasing = kwargs.get('increasing', True)
        self.duration = kwargs.get('duration', float('inf'))
        self.min_angle = kwargs.get('min_angle', 5)
        self.previous_max_angle = all_data['be'].max()
        self.previous_be = total_angle(values['be'], values['se0'], values['se1'])
    

    def algo(self, values, all_data):
        """
        Use the angular velosity to estimate the time to switch the posture
        """
        self.current_be = total_angle(values['be'], values['se0'], values['se1'])
        print 'Time: {:.2f}'.format(values['time']), 'Big encoder value: {:.2f}'.format(values['be'])
        
        if(sign_zero(self.previous_be)==-1 and self.previous_be - self.current_be <0):
            if(self.increasing == True):
                return 'seated'
            elif(self.increasing == False):
                return 'extended'
            self.previous_max_angle = self.previous_be
            print('max_angle', self.previous_be)
        elif(sign_zero(self.previous_be)==1 and self.previous_be - self.current_be >0):
            if(self.increasing == True):
                return 'extended'
            elif(self.increasing == False):
                return 'seated'
            self.previous_max_angle = self.previous_be
            print('max_angle', self.previous_be)
            

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
        
