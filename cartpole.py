import gym

env = gym.make("CartPole-v1")
obs = env.reset()

# Cart's horizontal position
# Velocity
# Angle of the pole
# Angular Velocity

img = env.render(mode = "rgb_array")
img.shape
