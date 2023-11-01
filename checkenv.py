from environment import WarehouseEnv

from stable_baselines3.common.env_checker import check_env


env = WarehouseEnv()

check_env(env)
