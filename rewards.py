import numpy as np

# rewards for all the states for making a movement
def discount_rewards(rewards, discount_rate):
    discounted_rewards = np.empty(len(rewards))
    cumilative_rewards = 0
    for step in reversed(range(len(rewards))):
        cumilative_rewards = rewards[step] + discount_rate * cumilative_rewards
        discounted_rewards[step] = cumilative_rewards
    return discounted_rewards

rewards = [10, 0, -50]
gamma = 0.8

print(discount_rewards(rewards, gamma))
        
    

