import os
from stable_baselines3.common.callbacks import BaseCallback


class TrainAndLoggingCallback(BaseCallback):
    def __init__(self, load_iterations, check_freq, save_path, model_name="PPO", verbose=0):
        super(TrainAndLoggingCallback, self).__init__(verbose)
        self.check_freq = check_freq
        self.save_path = save_path
        self.load_iterations = load_iterations
        self.model_name = model_name

    def _init_callback(self):
        if self.save_path is not None:
            os.makedirs(self.save_path, exist_ok=True)

    def _on_step(self):
        if self.n_calls % self.check_freq == 0:
            model_path = os.path.join(
                self.save_path, f"{self.model_name}_model_{self.load_iterations + self.n_calls}")
            self.model.save(model_path)
