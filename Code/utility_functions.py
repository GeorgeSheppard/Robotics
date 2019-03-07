from numpy import sin, cos, pi
import numpy
from os import listdir
from collections import OrderedDict
import datetime
import numpy as np


def flatten(values):
    final_list = []
    for list_value in values:
        if isinstance(list_value, list):
            [final_list.append(value) for value in list_value]
        else:
            final_list.append(list_value)
    return final_list


def read_file(filename):
    """
    Reads old data
    """
    data_type = current_data_types()

    # Data will be added to this with time
    all_data = numpy.empty((0, ), dtype=data_type)

    with open(filename, 'r') as f:
        file_data = f.read().split('\n')
        lines = [line.split(',') for line in file_data][:-1]
        for line in lines:
            all_data = numpy.append(all_data, numpy.array(
                [tuple(line)], dtype=data_type), axis=0)
    return all_data


def convert_read_numpy(data):
    data_type = current_data_types()
    # Data will be added to this with time
    all_data = numpy.empty((0, ), dtype=data_type)

    for i in xrange(len(data)):
        row = list(data[i])
        all_data = numpy.append(all_data, numpy.array(
            [tuple(row)], dtype=data_type), axis=0)
    return all_data


def current_data_types():
    return [('time', 'f4'), ('event', 'i4'), ('ax', 'f4'), ('ay', 'f4'), ('az', 'f4'), ('gx', 'f4'), ('gy', 'f4'),
            ('gz', 'f4'), ('se0', 'f4'), ('se1', 'f4'), ('se2',
                                                         'f4'), ('se3', 'f4'), ('be', 'f4'), ('av', 'f4'),
            ('cmx', 'f4'), ('cmy', 'f4'), ('algo', '|S25'), ('pos', '|S10')]


def get_latest_file(current_dir, test=True):
    """
    Get latest data file, if test = True will collect latest tst file, if not then only
    original files will be loaded
    current_dir:
        current directory: Code or Analysis
        test: include test files or not
    Returns:
        filename + ' Tst' or filename + ' Org'
    """
    if current_dir == 'Code':
        output_directory = 'Output_data/'
    else:
        output_directory = '../Output_data/'
    if test:
        filetype = 'Tst'
    else:
        filetype = 'Org'
    files = [name[:-4]
             for name in listdir(output_directory) if name[-3:] == filetype]
    if len(files) == 0:
        files = [name[:-4]
                 for name in listdir(output_directory) if name[-3:] == 'Org']
    dates = [datetime.datetime.strptime(
        ts, "%d-%m-%Y %H:%M:%S") for ts in files]
    dates.sort()
    latest = dates[-1]
    latest = datetime.datetime.strftime(latest, "%d-%m-%Y %H:%M:%S")
    if test:
        return latest + ' Tst', output_directory
    else:
        return latest + ' Org', output_directory


def convert_list_dict(current_values):
    """
    Converts list of values into a dictionary with keys of names current_data_types(), this way data
    can be accessed via values['time'] etc
    current_values: list of values with same length as current_data_types()
    """

    data_types = current_data_types()
    if len(current_values) != len(data_types):
        raise ValueError('Length of values not equal to data types length')
    values = OrderedDict()
    data_names = [key_pair[0] for key_pair in data_types]
    for i, name in enumerate(data_names):
        values[name] = current_values[i]
    return values


def cm_to_cartesian(angle1, angle2, angle3, position):
    """
    Returns cartesian coordinate of centre of mass of nao, with respect to the origin
    angles need to be in radians
    position is centre of mass from centre_of_mass_respect_seat
    """
    cartesian_position_seat = position_seat_cartesian(angle1, angle2, angle3)
    centre_of_mass_nao_seat = position

    # minus because of big encoder angle direction
    angle_seat = - \
        numpy.arctan(cartesian_position_seat[0]/cartesian_position_seat[1])

    # using rotation of axes formula to convert between frames of reference
    converted_coords_x = numpy.cos(
        angle_seat) * centre_of_mass_nao_seat[0] - numpy.sin(angle_seat) * centre_of_mass_nao_seat[1]
    converted_coords_y = numpy.sin(
        angle_seat) * centre_of_mass_nao_seat[0] + numpy.cos(angle_seat) * centre_of_mass_nao_seat[1]
    # adding cartesian positions together
    return [cartesian_position_seat[0] + converted_coords_x, cartesian_position_seat[1] + converted_coords_y]


def position_seat_cartesian(angle1, angle2, angle3):
    """
    Calculates the cartesian coordinate of the seat given all angles in radians
    angle1: big encoder
    angle2: small encoder 0
    angle3: small encoder 1
    """
    L1 = 1.5  # length of pendulum 1 in m
    L2 = 0.12  # length of pendulum 2 in m
    L3 = 0.20  # length of pendulum 3 in m
    x_seat = L3 * numpy.sin(angle1 + angle2 + angle3) + L2 * \
        numpy.sin(angle1 + angle2) + L1 * numpy.sin(angle1)
    y_seat = - L3 * numpy.cos(angle1 + angle2 + angle3) - L2 * \
        numpy.cos(angle1 + angle2) - L1 * numpy.cos(angle1)
    return [x_seat, y_seat]


def centre_of_mass_respect_seat(position, masses):
    """
    Returns centre of mass coordinates of nao in different positions, with respect to the SEAT
    """
    if position == "seated" and masses == False:
        x_com = (0.03674 - 0.03)
        y_com = (0.16 - 0.02463)
    elif position == "extended" and masses == False:
        x_com = (0.0488 - 0.03)
        y_com = (0.16 - 0.0124)
    elif position == 'raised' and masses == False:
        x_com = (0.0558 - 0.03)
        y_com = (0.16 - 0.000757)
    elif position == 'lowered' and masses == False:
        x_com = (0.031 - 0.03)
        y_com = (0.16 - 0.035)
    # need more elif's here for with masses
    else:
        raise ValueError("Position not found")
    return [x_com, y_com]


def moving_average(values, window_size):
    ma = [np.sum(values[i:i+window_size])/window_size for i,
          _ in enumerate(values[:-window_size+1])]
    return ma


def last_zero_crossing(values, previous_time, previous_be):
    """
    Interpolates between two times and big encoder values, should be used when sign
    of encoder changes.
    """
    current_be = values['be']
    dt = values['time'] - previous_time

    interpolate = dt * np.abs(current_be) / \
        np.abs(current_be - previous_be)

    min_time = values['time'] - interpolate
    return min_time


# def last_maxima(all_data, be_time='time', window_size=5):
#     # extracting a moving average of the previous encoder values to prevent incorrect maximas begin evaluated
#     # only use an odd number for window size, as indexes need to be adjusted below
#     avg_be = np.abs(moving_average(all_data['be'][-30:], window_size))
#     # extract index corresponding to latest maxima, index_max_angle(number of previous values to return)
#     angle_max_index = (np.diff(np.sign(np.diff(avg_be))) < 0).nonzero()[0] + 1 + (window_size - 1)/2
#     if be_time == 'time':
#         return all_data['time'][-30:][angle_max_index[-1]]
#     elif be_time == 'be':
#         return all_data['be'][-30:][angle_max_index[-1]]

def last_maxima(time, values, time_values='time', window_size=5):
    avg_values = np.abs(moving_average(values[-30:], window_size))
    max_index = (np.diff(np.sign(np.diff(avg_be))) < 0).nonzero()[0] + 1 + (window_size - 1)/2
    if time_values == 'time':
        return time[-30:][angle_max_index[-1]]
    else:
        return values[-30:][angle_max_index[-1]]


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

def total_angle(big_encoder, small_encoder1, small_encoder2):
    pass