import math
import numpy
import NumMod
import random
from Tkinter import *
import time

# Class to perform Q-Learning on a dumbbell pendulum to maximise the amplitude of the pendulum's swing


class QLearning:
    # initialise
    def __init__(self, mass, length, num_pos, alpha, gamma):
        # The mass of the system
        self.mass = mass
        # The length of the pendulum
        self.p_length = length
        # The number of states in the state space, defined by the possible positions of the robot
        self.num_positions = num_pos
        # The learning rate
        self.a = alpha
        # The discount factor
        self.g = gamma
        # The value of the torque exerted by moving both legs in Nm, as measured by the Robot subgroup
        torque = 8.66
        # The length of the robots legs in m, as measured by the Robot subgroup
        # This value is used as the length of the dumbbell
        leg_length = 0.1
        # The number of possible actions the robot can take
        self.num_actions = 3
        # The values of the torques of each of the actions in N
        self.actions = [-1 * torque / leg_length, 0, torque / leg_length]
        # The maximum value of the position of the robot
        self.max_pos = math.pi
        # The minimum value of the position of the robot
        self.min_pos = -1 * self.max_pos
        # The difference between two consecutive states in radians i.e. the value of one index
        self.one_pos = (self.max_pos - self.min_pos) / self.num_positions

        # To begin, set all Q-values to be zero
        self.q_values = numpy.zeros(shape = (self.num_positions, self.num_positions, self.num_actions))

        # Create the UI
        self.ui = Tk()
        self.ui_center = 200
        self.ui_canvas = Canvas(self.ui, width = self.ui_center * 2, height = self.ui_center * 2)
        self.ui_canvas.pack()
        # Create the pendulum
        pendulum_tip = self.ui_center + self.p_length * 100
        self.ui_pendulum = self.ui_canvas.create_line(self.ui_center, self.ui_center, self.ui_center, pendulum_tip)
        # Create the dumbbell
        self.ui_d_length = 0.5
        self.ui_d_angle = 0
        self.ui_dumbbell = self.ui_canvas.create_line(self.ui_center - 100 * self.ui_d_length / 2, pendulum_tip,
                                                      self.ui_center + 100 * self.ui_d_length / 2, pendulum_tip)
        # Create the labels and markers
        self.ui_iteration = self.ui_canvas.create_text(20, 20, text = str(-1))
        self.ui_dot_size = 5
        self.ui_pos_dot_1 = self.ui_canvas.create_oval(0, 0, 0, 0, fill = 'black')
        self.ui_pos_dot_2 = self.ui_canvas.create_oval(0, 0, 0, 0, fill = 'black')

    # Return the reward of a state
    # The reward of a state depends on the previous state, as the goal is to get higher, not reach a particular state
    def reward(self, initial_position, final_position):
        return (abs(final_position) - abs(initial_position)) * 10

    # Get the discrete index of a state
    def index_of_state(self, position):
        # If the state is out of bounds, raise an exception
        if position > self.max_pos or position < self.min_pos:
            raise IndexError

        # Convert the position into an index
        index = int(math.floor(position + self.max_pos / self.one_pos))

        # if (index == self.num_positions):
        #    index = self.num_positions - 1

        return index

    # Return the maximum Q-value of a state
    def max_q_value(self, state):
        # Get the index of the state
        state_index = self.index_of_state(state)
        # Set the first Q-value as the highest
        max_val = self.q_values[state_index][0][0]
        # Get the minimum and maximum positions where an action could be performed
        # If no force is applied, this will be approximately between the initial position and its mirror on the other
        # side of the pendulum
        min_action_pos = self.index_of_state(-1*abs(state))
        max_action_pos = self.index_of_state(abs(state))

        # For each action that can be performed, get the Q-value of the state-action pair and check if it's larger than
        # the current max
        for action_pos_index in range(min_action_pos, max_action_pos):
            for action_index in range(1, self.num_actions):
                q = self.q_values[state_index][action_pos_index][action_index]
                if q > max_val:
                    max_val = q

        # Return the maximum qvalue
        return max_val

    # Return the x co-ordinate of the end of the pendulum, given its angle
    def ui_x_pos(self, angle):
        return self.ui_center + self.p_length * math.sin(angle) * 100

    # Return the x co-ordinate of the end of the pendulum, given its angle
    def ui_y_pos(self, angle):
        return self.ui_center + self.p_length * math.cos(angle) * 100

    # Move the dumbbell to its new position given the last action performed
    def ui_move_dumbbell(self, position, action):
        # The center of the dumbbell
        centerx = self.ui_x_pos(position)
        centery = self.ui_y_pos(position)
        # Get the direction of the action
        direction = 1
        if action < 0:
            direction = -1
        # Update the angle of the dumbbell
        if action != 0:
            self.ui_d_angle += direction * math.pi / 6
        # Update the dumbbell's position
        x1 = centerx - self.ui_d_length * math.cos(self.ui_d_angle) * 100
        x2 = centerx + self.ui_d_length * math.cos(self.ui_d_angle) * 100
        y1 = centery - self.ui_d_length * math.sin(self.ui_d_angle) * 100
        y2 = centery + self.ui_d_length * math.sin(self.ui_d_angle) * 100
        self.ui_canvas.coords(self.ui_dumbbell, x1, y1, x2, y2)

    # Perform an action in a state and update the Q-value of the state-action pair
    # If action_pos_index or action is -1, a random value will be selected
    # If ui is 0 the UI won't be shown
    def perform_action(self, position, action_pos_index, action, iteration, ui):
        # If the UI is enabled, update it
        if ui:
            # Indicate the iteration
            self.ui_canvas.itemconfigure(self.ui_iteration, text=str(iteration))
            # Show the amplitude of the first swing on both sides of the pendulum
            x_pos_1 = self.ui_x_pos(position)
            x_pos_2 = 2*self.ui_center - x_pos_1
            y_pos = self.ui_y_pos(position)
            self.ui_canvas.coords(self.ui_pos_dot_1, x_pos_1, y_pos, x_pos_1 + self.ui_dot_size, y_pos + self.ui_dot_size)
            self.ui_canvas.coords(self.ui_pos_dot_2, x_pos_2, y_pos, x_pos_2 + self.ui_dot_size, y_pos + self.ui_dot_size)
            # Move the dumbbell to the correct position
            self.ui_move_dumbbell(position, 0)

        # Get the index of this state
        state_index = self.index_of_state(position)

        # Generate a random action if specified
        if action_pos_index == -1:
            minposac = self.index_of_state(-1*abs(position))
            action_pos_index = int(math.floor(random.random() * (self.num_positions - state_index * 2) + minposac))
        if action == -1:
            action = int(math.floor(random.random() * self.num_actions))

        # The current values of the position and velocity
        current_position = position
        current_velocity = 0

        # Variables to keep track of where the pendulum is and if it has completed one swing
        first_velocity = NumMod.NextVelocity(position, 0, 0, self.mass, self.p_length)
        passed_middle = 0
        changed_direction = 0

        # For the duration of this swing
        while changed_direction == 0:
            # Get the torque of the action to be performed on this iteration
            if self.index_of_state(current_position) == action_pos_index:
                this_action = self.actions[action]
            else:
                this_action = 0
            # Apply this torque to the dumbbell using the numerical model
            next_position = NumMod.NextPosition(current_position, current_velocity, this_action, self.mass, self.p_length)
            next_velocity = NumMod.NextVelocity(current_position, current_velocity, this_action, self.mass, self.p_length)

            # Keep track of the pendulum's position
            # It has finished this swing once it has passed 0 and changed the direction of its motion
            if next_position * position < 0:
                passed_middle = 1
            if passed_middle == 1 and next_velocity * first_velocity < 0:
                changed_direction = 1

            # Update the current position and velocity
            current_position = next_position
            current_velocity = next_velocity

            if ui:
                # Update the UI
                x = self.ui_x_pos(current_position)
                y = self.ui_y_pos(current_position)
                self.ui_canvas.coords(self.ui_pendulum, self.ui_center, self.ui_center, int(x), int(y))
                self.ui_move_dumbbell(next_position, this_action)
                self.ui.update()
                time.sleep(0.01)

            # If the action causes the pendulum to make a full rotation, the action was not good and the position
            # should be reset
            if current_position < self.min_pos or current_position > self.max_pos:
                self.q_values[state_index][action_pos_index][action] = -10
                return self.max_pos + 1

        # Calculate and update the Q-value
        current = self.q_values[state_index][action_pos_index][action]
        new_q_value = current + self.a * (self.reward(position, current_position) + self.g * self.max_q_value(current_position) - current)
        self.q_values[state_index][action_pos_index][action] = new_q_value

        # Return the resulting position
        return current_position

    # Returns the position and value of the action with the highest Q-value
    def best_action(self, state_index):
        # Set the maximum value to be the first one
        pos = 0
        value = 0
        max_value = self.q_values[state_index][pos][value]

        min_action_pos = state_index
        max_action_pos = self.num_positions - state_index
        if min_action_pos > max_action_pos:
            min_action_pos = self.num_positions - state_index
            max_action_pos = state_index

        # For each action, get its Q-value and check if it's larger than the current maximum
        for action_pos_index in range(min_action_pos, max_action_pos):
            for action_index in range(1, self.num_actions):
                q_value = self.q_values[state_index][action_pos_index][action_index]
                if q_value > max_value:
                    max_value = q_value
                    pos = action_pos_index
                    value = action_index

        return pos, value