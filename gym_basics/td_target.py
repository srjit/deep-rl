
import itertools
import gym
import numpy as np
import plotting
import sys
import sklearn.pipeline
import sklearn.preprocessing


__author__ = "Sreejith Sreekumar"
__email__ = "sreekumar.s@husky.neu.edu"
__version__ = "0.0.1"


env = gym.envs.make("MountainCar-v0")

from sklearn.linear_model import SGDRegressor

from sklearn.kernel_approximation import RBFSampler
from sklearn.kernel_approximation import Nystroem

observation_examples = np.array([env.observation_space.sample() for x in range(10000)])
scaler = sklearn.preprocessing.StandardScaler()
scaler.fit(observation_examples)

featurizer = sklearn.pipeline.FeatureUnion([
        ("rbf1", RBFSampler(gamma=5.0, n_components=100)),
        ("rbf2", RBFSampler(gamma=2.0, n_components=100)),
        ("rbf3", Nystroem(gamma=1.0, n_components=100)),
        ("rbf4", Nystroem(gamma=0.5, n_components=100))
        ])

featurizer.fit(scaler.transform(observation_examples))


class Estimator:

    def __init__(self):
        self.models = []

        for _ in range(env.action_space.n):
            model = SGDRegressor(learning_rate="constant")
            model.partial_fit([self.featurize_state(env.reset())], [0])

            self.models.append(model)

    def featurize_state(self, state):
        return featurizer.transform(scaler.transform([state]))[0]

    def update(self, s, a, y):
        features = self.featurize_state(s)
        self.models[a].partial_fit([features], [y])
                                        
    def predict(self, s,  a=None):
        '''
        predict returns 
        '''
        features = self.featurize_state(s)
        if not a:
            return np.array([m.predict([features])[0] for m in self.models])
        else:
            return self.models[a].predict([features])[0]        


def epsilon_greedy_policy(estimator, epsilon, nA):

    def policy(observation):
        A = np.ones(nA, dtype=float) * epsilon / nA
        q_values =  estimator.predict(observation)
        best_action = np.argmax(q_values)
        A[best_action] += (1.0 - epsilon)
        return A

    return policy

def q_learning(env, estimator, num_episodes, discount_factor=1.0, epsilon=0.1, epsilon_decay=1.0):

    stats = plotting.EpisodeStats(
        episode_lengths=np.zeros(num_episodes),
        episode_rewards=np.zeros(num_episodes)        
    )

    for episode_id in range(num_episodes):

        policy = epsilon_greedy_policy(estimator, epsilon * epsilon_decay**episode_id, num_episodes)

        last_reward = stats.episode_rewards[episode_id - 1]
        sys.stdout.flush()

        state = env.reset()

        next_action = None

        # take a step
        for t in itertools.count():

            if next_action is None:
                action_probabilities = policy(state)
                action = np.random.choice(np.arange(len(action_probabilities)), p=action_probabilities)
            else:
                action = next_action

            next_state, reward, done, _  = env.step(action)
            
            stats.episode_rewards[episode_id] += reward
            stats.episode_lengths[episode_id] = t
            
            q_values_next = estimator.predict(next_state)
            td_target = reward + discount_factor * q_values_next
            
            estimator.update(state, action, td_target)

            print("\rStep {} @ Episode {}/{} ({})".format(t, episode_id + 1, num_episodes, last_reward), end="")

            if done:
                break            

            state = next_state
    
    return stats


estimator = Estimator()

stats = q_learning(env, estimator, 100, epsilon=0.0)

