import QLearningUI as QL
import random


def main():
    q_learning = QL.QLearning(5.18, 1.82, 501, 0.5, 0.9)
    # Do some random Q-Learning
    for num1 in range(0, 10000):
        # Reset the dumbbell angle
        q_learning.ui_d_angle = 0
        # Get a random position
        position = random.random() * q_learning.num_positions * q_learning.one_pos - q_learning.max_pos
        # Make sure the position is not too small; the algorithm has difficulty learning if the pendulum starts too close to rest
        while abs(position) < 0.1:
            position = random.random() * q_learning.num_positions * q_learning.one_pos - q_learning.max_pos
        # Learn for 10 swings
        for num2 in range(0, 10):
            position = q_learning.perform_action(position, -1, -1, -1, 0)
            # Correct the position if it goes out of bounds
            while position > q_learning.max_pos:
                position = position - q_learning.max_pos
            while position < q_learning.min_pos:
                position = position + q_learning.max_pos

    print q_learning.q_values.astype(int)

    # Show the UI implementing the learnt Q-values
    for num1 in range(0, 10000):
        # Reset the dumbbell angle
        q_learning.ui_d_angle = 0
        # Get a random position
        position = random.random() * q_learning.num_positions * q_learning.one_pos - q_learning.max_pos
        # Make sure the position is not too small; the algorithm has difficulty learning if the pendulum starts too close to rest
        while abs(position) < 0.1:
            position = random.random() * q_learning.num_positions * q_learning.one_pos - q_learning.max_pos
        # Learn for 10 swings
        for num2 in range(0, 10):
            pos_index = q_learning.index_of_state(position)
            action_pos, action = q_learning.best_action(pos_index)
            position = q_learning.perform_action(position, action_pos, action, num1, 1)
            # Correct the position if it goes out of bounds
            while position > q_learning.max_pos:
                position = position - q_learning.max_pos
            while position < q_learning.min_pos:
                position = position + q_learning.max_pos

main()