import os
import sys
import time
from datanames import values
from naoqi import ALProxy
from change_stiffness import *
from positionvalues import extended, seated
ROBOT_IP = "192.168.1.3"
PORT = 9559


class Robotcontrol():
    def __init__(self, ROBOT_IP="192.168.1.2", PORT=9559):
        self.motion = ALProxy("ALMotion", ROBOT_IP, PORT)
        self.memory = ALProxy("ALMemory", ROBOT_IP, PORT)

    def get_angle(self, nameofpart):
        a = self.memory.getData(values[str(nameofpart)][1])
        name = values[str(nameofpart)][0]
        return a, name

    #motion.setStiffnesses("Body", 1)
    # change_stiffness('stiffen')
    # print get_angle('BC')

    def initial_seated_position(self):
        parts = ["Head", "RLeg", "LLeg"]
        self.motion.setStiffnesses(parts, 1.0)  # stiffen
        angle_names = [
            values['HP'][0],
            values['RHP'][0],
            values['LHP'][0],
            values['RKP'][0],
            values['LKP'][0]]
        angles = [-0.6, -0.51, -0.51, -0.09, -0.09]
        speed = 0.5
        self.motion.setAngles(angle_names, angles, speed)

    # initial_seated_position()
    # print motion.getSummary()
    # knee range is longest so normalise based on this parameter

    def move_part(self, parts, angle_names, angles, speed, rest_time):
        self.motion.setStiffnesses(parts, 1.0)
        self.motion.setAngles(angle_names, angles, speed)
        time.sleep(rest_time)

    def extended_position(self):
        angle_names = extended.keys()
        angles = extended.values()
        rest_time = 0
        parts = ["Head", "RArm", "LArm", "RLeg", "LLeg"]
        final_angle_names = [values[name][0] for name in angle_names]
        #speed =       [normalise_speed()]
        self.move_part(parts, final_angle_names, angles, 0.3, rest_time)

    def seated_position(self):
        rest_time = 0
        parts = ["Head", "RArm", "LArm", "RLeg", "LLeg"]
        angle_names = seated.keys()
        angles = seated.values()
        final_angle_names = [values[name][0] for name in angle_names]
        self.move_part(parts, final_angle_names, angles, 0.3, rest_time)

    def record_data(self, nameofpart):
        """ records the data from ALMemory.
        Returns a matrix of the values

        """
        print "Recording data from NAO..."

        output = os.path.abspath('Output_data/record_data.csv')

        with open(output, "w") as fp:
            for i in range(1, 100):
                value = self.get_angle(str(nameofpart))
                fp.write(", ".join(str(x) for x in value) + "\n")
                time.sleep(0.05)

        print "Results written to", output



    def normalisespeed(nameofpart):
        '''Normalise speed of NAO's based on the knee range and speed which is the slowest part'''
        knee_speed = 1
        knee_range = 
        part_range =
        partspeed = knee_speed*(part_range/knee_range)
        return part_speed





    def test_move_part(self):
        self.motion.setStiffnesses("RLeg", 1.0)
        self.motion.setStiffnesses("LLeg", 1.0)
        self.motion.setAngles("LKneePitch", 0.800258815289, 0.1)
        # motion.setAngles("LAnklePitch",-1.18943989277,0.1)
        self.motion.setAngles("RKneePitch", 0.800258815289, 0.1)
        # motion.setAngles("RAnklePitch",-1.18943989277,0.1)
    def summary(self):
        print self.motion.getSummary()

#print 6
r = Robotcontrol(ROBOT_IP="192.168.1.3", PORT=9559)
#r.move_part("Body", "LHand", 0,0.5, 0)
#print 1
#r.extended_position()
#try:
#    while True:
#        a = raw_input("extend")
#        b = raw_input("sit")
#        r.seated_position()

#except KeyboardInterrupt:
 #   pass
r.summary()