from robot_interface import Robot
from encoder_interface import Encoders

from sys import path
path.insert(0, 'Single_Pendulum')
from single_startup_const_period import Start
from single_stop_const_period import Stop
from single_increase_quarter_period import IncreaseQuarterPeriod, DecreaseQuarterPeriod
from single_increase_parametric_rework import IncreaseParametric, DecreaseParametric
from single_maintain_constant import MaintainConstant
from single_nothing import Nothing
from single_increase_angular_velocity import IncreaseAngularVelocity


class Algorithm(Robot, Encoders):
    """
    This is an example algorithm class, as everyone will be working on different algorithms
    """

    def __init__(self, BigEncoder, SmallEncoders, values, positions, ALProxy):
        # Initialise encoder
        Encoders.__init__(self, BigEncoder, SmallEncoders, small_encoders_required=False)
        # Initialise robot
        Robot.__init__(self, values, positions, ALProxy, masses=True)

        #self.order = [{
            #'algo': Start,
            #'duration': 25.0
        #},{
            #'algo': IncreaseQuarterPeriod,
            #'max_angle': 15
        #},{
            #'algo': DecreaseQuarterPeriod,
            #'min_angle': 10
        #},{
            #'algo': IncreaseParametric,
            #'duration': 80
        #},{
            #'algo': DecreaseParametric,
            #'min_angle': 5.0
        #},{
            #'algo': Stop,
            #'min_angle': 1.0
        #},{
            #'algo': Nothing
        #}]
        
        #self.order = [{
            #'algo': Nothing,
            #'duration': 10
        #},{
            #'algo': Stop,
            #'min_angle': 1.0
        #},{
            #'algo': Nothing
        #}]
        
        self.order = [{
            'algo': Nothing,
            'duration': 5
        },{
            'algo': IncreaseAngularVelocity,
            'duration': 4
        }]
        
        #self.order = [{
            #'algo': Nothing,
            #'duration': 5.0
        #},{
            #'algo': MaintainConstant,
            #'max_angle': 10,
            #'duration': 60
        #}]
        
        #self.order = [{
            #'algo': Nothing,
            #'duration': 5.0
        #},{
            #'algo': MaintainConstant,
            #'max_angle': 10.0,
            #'duration': 60.0
        #}]
        
        #self.order = [{
            #'algo': Nothing,
            #'duration': 5.0
        #},{
            #'algo': IncreaseQuarterPeriod,
            #'duration': 120.0
        #}]
