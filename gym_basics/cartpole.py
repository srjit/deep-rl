import gym

__author__ = "Sreejith Sreekumar"
__email__ = "sreekumar.s@husky.neu.edu"
__version__ = "0.0.1"


env = gym.make("CartPole-v0")


for e_index in range(20):

    observation = env.reset()
    for t in range(100):
        env.render()

        print(observation)
        action = env.action_space.sample()
        import ipdb
        ipdb.set_trace()
        observation, reward, done, info = env.step(action)
        if done:
            print("Episode finished after {} timesteps".format(t+1))
            break
        
    
