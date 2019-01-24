"""
Author: Chris Patmore
Date: 22/03/2017
Description: The implementation of a DQN agent
"""
from copy import deepcopy
from keras.models import Sequential
import numpy as np
import time

# the Q network, important stuff


class DeepQNetwork(object):

    # constructor initialises the network with the given parameters
    def __init__(self, model, policy, number_actions, memory, gamma,
                 batch_size, environment, min_action, initial_tau, tau_decay_rate):

        self.model = model                    # the network model
        self.policy = policy                  # action selection policy
        self.number_actions = number_actions  # max no. discrete actions
        self.memory = memory                  # replay memory
        self.gamma = gamma                    # discount factor
        self.batch_size = batch_size          # size of training batches
        self.environment = environment        # simulation environment
        self.min_action = min_action          # min discrete action
        self.tau = initial_tau                # initial policy tau
        self.tau_decay_rate = tau_decay_rate  # tau decay rate
        self.last_observation = None          # initial state
        self.last_action = None               # initial state

    # convenience method to convert to the correct input for the
    # environments step method
    def process_action(self, action):
        correction = action*(2*abs(self.min_action))/(self.number_actions-1)
        action = self.min_action + correction
        return [action]

    # convenience method to prepare for keras methods
    def process_state(self, state):
        state = np.array(state)
        return state

    # use the network to compute the Q-values for a state
    def compute_q_values(self, state):
        state = self.process_state(state)
        q_values = self.model.predict_on_batch(state).flatten()

        return q_values

    # compile the model so it can be used, copy weights onto target network
    def compile(self, optimizer):
        config = self.model.get_config()
        self.target_model = Sequential.from_config(config)
        self.target_model.compile(optimizer, loss='mse')
        self.model.compile(optimizer, loss='mse')
        self.target_model.set_weights(self.model.get_weights())

    # load network weights from a save file, onto both networks
    def load_weights(self, filepath):
        self.model.load_weights(filepath)
        self.target_model.set_weights(self.model.get_weights())

    # save network weights to a file
    def save_weights(self, filepath, overwrite=False):
        self.model.save_weights(filepath, overwrite=overwrite)

    # reset known state information
    def reset(self):
        self.last_observation = None
        self.last_action = None

    # select and action using the policy
    def select_action(self, state):
        q_values = self.compute_q_values([[state]])   # convert state into right form for keras
        action = self.policy.select_action(q_values=q_values)

        self.last_observation = state
        self.last_action = action

        return action

    # update the network with some experiences in one gradient update
    def update_net(self, reward, state):
        # add the most recent experience
        self.memory.add(self.last_observation, self.last_action, reward, state)

        # get a batch of experiences from memory
        start_state_batch, action_batch, reward_batch, final_state_batch = self.memory.sample(self.batch_size)

        # state batches are re-shaped to function with keras methods
        start_state_batch = np.array([start_state_batch]).reshape((-1, 1, self.environment.observation_space.shape[0]))
        final_state_batch = np.array([final_state_batch]).reshape((-1, 1, self.environment.observation_space.shape[0]))

        # compute the q-values for the next state using target Network
        next_state_q_values = self.target_model.predict_on_batch(final_state_batch)
        # compute the q-values for the current state using Q-Network
        current_state_q_values = self.model.predict_on_batch(start_state_batch)

        # using Q-value algorithm compute new q value for state action pair
        q_batch = np.max(next_state_q_values, axis=1).flatten()  # best action in next state
        discounted_reward_batch = self.gamma * q_batch           # discount the action
        q_update = reward_batch + discounted_reward_batch        # Q-values updates

        # replace the q value for the action taken with the new value
        for idx, (current_state, action, Q) in enumerate(zip(current_state_q_values, action_batch, q_update)):
            current_state[action] = Q

        # single gradient train with states and altered q-values
        self.model.train_on_batch(start_state_batch, current_state_q_values)

    # train the network with the environment
    def train(self, episodes, steps, visualize=False):
        # intialisations for training
        print('training for %s episodes' % episodes)
        file = open('Training_Rewards_NRDumbbell0Start.txt', 'w')
        start = time.time()
        all_episode_rewards = []

        # for each episode
        for episode in range(episodes):
            # reset the environment
            current_state = deepcopy(self.environment.reset())
            episode_reward = 0
            # visualize if desired
            if visualize:
                self.environment.render()

            # print the current episode
            print("Episode #: %s" % (episode,))

            # for every step in an episode
            for step in range(steps):
                # select and perform an action
                action = self.select_action(current_state)
                new_state, reward, done, info = self.environment.step(self.process_action(action))
                episode_reward += reward
                # for GUI
                if visualize:
                    self.environment.render()

                # update the network with the results
                self.update_net(reward, new_state)
                if done:
                    break
                # progress the state of the environment
                current_state = deepcopy(new_state)

            # print to screen
            file.write('%s\t%s\n' % (episode, episode_reward))
            all_episode_rewards.append(episode_reward)
            # update target model
            if episode % 1 == 0:
                self.target_model.set_weights(self.model.get_weights())

            # decay tau to 1 following rate
            if self.tau > 1.:
                self.tau = self.tau/self.tau_decay_rate
            if self.tau < 1.:
                self.tau = 1.
            self.policy.set_tau(self.tau)


        # end of training stats
        end = time.time()
        file.close()
        # Rolling reward
        file = open('Training_Rolling_Rewards_NRDumbbell0Start.txt', 'w')
        summing = 0
        for i in range(episodes):
            summing += all_episode_rewards[i]
            if (i + 1) % 10 == 0:
                file.write('%s\t%s\n' % (i-5, summing/10))
                summing = 0
        file.close()
        print('Time to complete training of %s episodes: %r seconds' % (episodes, (end-start)))

    # test the trained network on the environment
    def test(self, episodes, steps, visualize=True):
        # set tau low for test
        self.tau = 1
        self.policy.set_tau(self.tau)
        print('Testing for %s episodes' % episodes)
        rewards = []

        # for each episode
        for episode in range(episodes):
            episode_reward = 0
            # reset
            current_state = deepcopy(self.environment.reset())
            if visualize:
                self.environment.render()

            # print the episode
            print("Episode #: %s" % (episode,))
            # perform each step
            for step in range(steps):
                # select and perform an action
                action = self.select_action(current_state)

                new_state, reward, done, info = self.environment.step(self.process_action(action))
                episode_reward += reward
                if visualize:
                    self.environment.render()
                if done:
                    break

                # progress the state of the environment
                current_state = deepcopy(new_state)
            rewards.append(episode_reward)
            print('Episode reward : %r' % episode_reward)

        # test statistics, these fo not work for python 2
        try:
            import statistics
            print('Average reward : %r +/- %r' % (statistics.mean(rewards), statistics.stdev(rewards)))
        except ImportError:
            print('No Statistics in python 2')
