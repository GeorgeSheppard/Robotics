"""
Contains class that mocks how naoqi connects to robot etc, then interface
can run away from robot if this is imported as substitute for naoqi.

Contains:
    ALProxy
"""
from sys import path
path.insert(0, '../')
from limb_data import values

position = {}

class ALProxy():
    def __init__(self, name, ip, port):
        pass
        
    def say(self, word):
        print 'NAO: ', word

    def getData(self, key):
        if key in position.keys():
            return position[key]
        else:
            return 1

    def setStiffness(self, parts, stiffness):
        pass

    def setStiffnesses(self, parts, speed):
        pass

    def setAngles(self, names, angles, speed):
        for key in values.keys():
            if values[key][0] == names:
                position[values[key][1]] = angles

    def setFallManagerEnabled(self, boolean):
        pass
