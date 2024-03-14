import glob
import pickle
import lcm
import sys

from rl_sim2real.utils.deployment_runner import DeploymentRunner
from rl_sim2real.envs.lcm_agent import LCMAgent
from rl_sim2real.utils.cheetah_state_estimator import StateEstimator
from rl_sim2real.utils.command_profile import *

import pathlib
import os

lc = lcm.LCM("udpm://239.255.76.67:7667?ttl=255")

def load_and_run_policy(experiment_name, max_vel=1.0, max_yaw_vel=1.0, max_vel_probe=1.0):
    # load agent
    # logdir = glob.glob(f"../../exported/")
    logdir = "../../exported/"

    with open(os.path.join(logdir) + "cfg.pkl", 'rb') as file:
        cfg = pickle.load(file)
        print(cfg.keys())

    print('Config successfully loaded!')

    se = StateEstimator(lc)

    control_dt = 0.02
    command_profile = RCControllerProfile(dt=control_dt, state_estimator=se, x_scale=max_vel, y_scale=0.6, yaw_scale=max_yaw_vel, probe_vel_multiplier=(max_vel_probe / max_vel))

    hardware_agent = LCMAgent(cfg, se, command_profile)
    se.spin()

    from rl_sim2real.envs.history_wrapper import HistoryWrapper
    hardware_agent = HistoryWrapper(hardware_agent)
    from rl_sim2real.envs import observation_buffer
    history_obs_buf = observation_buffer.ObservationBuffer(1, cfg["env"]["num_observations"] - 3, cfg["env"]["include_history_steps"], 'cuda:0')

    print('Agent successfully created!')

    policy = load_policy(logdir)
    print('Policy successfully loaded!')
    print(se.get_gravity_vector())

    # load runner
    root = f"{pathlib.Path(__file__).parent.resolve()}/../logs/"
    pathlib.Path(root).mkdir(parents=True, exist_ok=True)
    deployment_runner = DeploymentRunner(experiment_name=experiment_name, se=None,
                                         log_root=f"{root}/{experiment_name}")
    deployment_runner.add_control_agent(hardware_agent, "hardware_closed_loop")
    deployment_runner.add_policy(policy)
    deployment_runner.add_command_profile(command_profile)

    if len(sys.argv) >= 2:
        max_steps = int(sys.argv[1])
    else:
        max_steps = 10000000
    print(f'max steps {max_steps}')

    deployment_runner.run(history_obs_buf, max_steps=max_steps, logging=True)

def load_policy(logdir):
    actor = torch.jit.load(logdir + 'actor.pt').to('cuda:0')
    encoder = torch.jit.load(logdir + 'encoder.pt').to('cuda:0')
    vq_layer = torch.jit.load(logdir + 'vq_layer.pt').to('cuda:0')

    def policy(obs, info):
        encoding = encoder(obs["obs_history"].to('cuda:0'))
        z = vq_layer(encoding)
        action = actor(torch.cat((obs["obs"].to('cuda:0'), z), dim=-1)).to('cpu')
        info['z'] = z.to('cpu')
        return action

    return policy


if __name__ == '__main__':
    experiment_name = "a1_blinddog"

    load_and_run_policy(experiment_name=experiment_name, max_vel=3.0, max_yaw_vel=5.0, max_vel_probe=1.0)
