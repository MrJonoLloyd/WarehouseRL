import os
from environment import WarehouseEnv
from callback import TrainAndLoggingCallback
from stable_baselines3 import DQN, PPO

CHECKPOINT_DIR = './train'
LOG_DIR = './logs/'

LOAD_ITERATION = 21000000
TIME_STEPS = 25000000
MODEL_NAME = "big_PPO"

PLAYER_TEST = 0
CREATE_MODEL = 0
LOAD_MODEL = 1
TRAIN_MODEL = 0
TEST_MODEL = 1


if __name__ == "__main__":
    render_mode = None
    if TEST_MODEL:
        render_mode = "human"
    env = WarehouseEnv(render_mode=render_mode)

    # --------------------

    # Testing Random inputs
    if PLAYER_TEST:
        for episode in range(5):
            obs = env.reset()
            done = False
            total_reward = 0

            while not done:
                action = int(input())
                obs, reward, done, trunc, info = env.step(action)
                total_reward += reward
            print(f"Total Reward for episode {episode} is {total_reward}")

    # --------------------

    # Creating Model
    if CREATE_MODEL:
        LOAD_ITERATION = 0
        model = PPO('MlpPolicy', env, tensorboard_log=LOG_DIR,
                    verbose=1)

    # --------------------

    # Loading model
    if LOAD_MODEL:
        model = PPO.load(os.path.join(
            CHECKPOINT_DIR, f'./{MODEL_NAME}_model_{LOAD_ITERATION}'), env=env)

    # --------------------

    # # Training the model
    if TRAIN_MODEL:
        callback = TrainAndLoggingCallback(
            check_freq=100000, save_path=CHECKPOINT_DIR, model_name=MODEL_NAME, load_iterations=LOAD_ITERATION)
        model.learn(total_timesteps=TIME_STEPS, callback=callback)

    # --------------------

    # Testing the model
    if TEST_MODEL:
        for episode in range(10):
            obs = env.reset()[0]
            done = False
            total_reward = 0

            while not done:
                action, _ = model.predict(obs)
                obs, reward, done, trunc, info = env.step(int(action))
                total_reward += reward
            print(f"Total Reward for episode {episode} is {total_reward}")
