# Dictionary to access the part names and sensor values for NAO including ranges of motion.
# 'ID' = part name, path name for parts and sensors, minimum angle (rad), maximum angle(rad), range of motion, range between seated and extended positions (rad)

values = {
    'AX': ['AngleX', 'Device/SubDeviceList/InertialSensor/AngleX/Sensor/Value'],
    'AY': ['AngleY', 'Device/SubDeviceList/InertialSensor/AngleY/Sensor/Value'],
    'AZ': ['AngleZ', 'Device/SubDeviceList/InertialSensor/AngleZ/Sensor/Value'],
    'GX': ["GyroscopeX", "Device/SubDeviceList/InertialSensor/GyroscopeX/Sensor/Value"],
    'GY': ["GyroscopeY", "Device/SubDeviceList/InertialSensor/GyroscopeY/Sensor/Value"],
    'GZ': ["GyroscopeZ", "Device/SubDeviceList/InertialSensor/GyroscopeZ/Sensor/Value"],
    'ACX': ["AccelerometerX", "Device/SubDeviceList/InertialSensor/AccelerometerX/Sensor/Value"],
    'ACY': ["AccelerometerY", "Device/SubDeviceList/InertialSensor/AccelerometerY/Sensor/Value"],
    'ACZ': ["AccelerometerZ", "Device/SubDeviceList/InertialSensor/AccelerometerZ/Sensor/Value"],
    'BC': ["Battery", "Device/SubDeviceList/Battery/Charge/Sensor/Value"],
    'HY': ["HeadYaw", "Device/SubDeviceList/HeadYaw/Position/Sensor/Value", -2.0857, 2.0857, 4.1714, 1],
    'HP': ["HeadPitch", "Device/SubDeviceList/HeadPitch/Position/Sensor/Value", -0.6720, 0.5149, 1.1869, 1.119454],
    'RSR': ["RShoulderRoll", "Device/SubDeviceList/RShoulderRoll/Position/Sensor/Value", -1.3265, 0.3142, 1.6407, 0.30612],
    'RSP': ["RShoulderPitch", "Device/SubDeviceList/RShoulderPitch/Position/Sensor/Value", -2.0857, 2.0857, 4.1714, 0.5933189999],
    'RER': ["RElbowRoll", "Device/SubDeviceList/RElbowRoll/Position/Sensor/Value", 0.0349, 1.5446, 1.5097, 1.31135],
    'REY': ["RElbowYaw", "Device/SubDeviceList/RElbowYaw/Position/Sensor/Value", -2.0857, 2.0857, 4.1714, 0.05078999999],
    'RWY': ["RWristYaw", "Device/SubDeviceList/RWristYaw/Position/Sensor/Value", -1.8238, 1.8238, 3.6476, 0.0061399999],
    'RH': ["RHand", "Device/SubDeviceList/RHand/Position/Sensor/Value", 0, 0.00860, 1, 1],
    'RHYP': ["RHipYawPitch", "Device/SubDeviceList/RHipYawPitch/Position/Sensor/Value", -1.145303, 0.740810, 1.886113, 1],
    'RHP': ["RHipPitch", "Device/SubDeviceList/RHipPitch/Position/Sensor/Value", -1.535889, 0.484090, 2.019979, 0.486270000000000],
    'RHR': ["RHipRoll", "Device/SubDeviceList/RHipRoll/Position/Sensor/Value", -0.790477, 0.379472, 1.169949, 1],
    'RKP': ["RKneePitch", "Device/SubDeviceList/RKneePitch/Position/Sensor/Value", -0.103083, 2.120198, 2.223281, 1.492079999],
    'RAP': ["RAnklePitch", "Device/SubDeviceList/RAnklePitch/Position/Sensor/Value", -1.186448, 0.932056, 2.118504, 0.922747],
    'RAR': ["RAnkleRoll", "Device/SubDeviceList/RAnkleRoll/Position/Sensor/Value", -0.768992, 0.397935, 1.166927, 1],
    'LSR': ["LShoulderRoll", "Device/SubDeviceList/LShoulderRoll/Position/Sensor/Value", -0.3142, 1.3265, 1.6407, 0.40191200000000],
    'LSP': ["LShoulderPitch", "Device/SubDeviceList/LShoulderPitch/Position/Sensor/Value", -2.0857, 2.0857, 4.1714, 0.35589000000000],
    'LER': ["LElbowRoll", "Device/SubDeviceList/LElbowRoll/Position/Sensor/Value", -1.5446, -0.0349, 1.5795, 1.27621],
    'LEY': ["LElbowYaw", "Device/SubDeviceList/LElbowYaw/Position/Sensor/Value", -2.0857, 2.8057, 4.1714, 0.0046000000000001595],
    'LWY': ["LWristYaw", "Device/SubDeviceList/LWristYaw/Position/Sensor/Value", -1.8238, 1.8238, 3.6476, 0.141131999999],
    'LH': ["LHand", "Device/SubDeviceList/LHand/Position/Sensor/Value", 0, 0.00860, 1, 1],
    'LHYP': ["LHipYawPitch", "Device/SubDeviceList/LHipYawPitch/Position/Sensor/Value", -1.145303, 0.740810, 1.886113],
    'LHP': ["LHipPitch", "Device/SubDeviceList/LHipPitch/Position/Sensor/Value", -1.535889, 0.484090, 2.019979, 0.486270000000000],
    'LHR': ["LHipRoll", "Device/SubDeviceList/LHipRoll/Position/Sensor/Value", -0.379472, 0.790477, 1.169949],
    'LKP': ["LKneePitch", "Device/SubDeviceList/LKneePitch/Position/Sensor/Value", -0.092346, 2.112528, 2.204874, 1.492079999],
    'LAP': ["LAnklePitch", "Device/SubDeviceList/LAnklePitch/Position/Sensor/Value", -1.189516, 0.922747, 2.112263, 0.922747],
    'LAR': ["LAnkleRoll", "Device/SubDeviceList/LAnkleRoll/Position/Sensor/Value", -0.397880, 0.769001, 1.166881, 1]
}
