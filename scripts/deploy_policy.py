import glob
import pickle as pkl
import lcm
import sys

from dog_rl_deploy.utils.deployment_runner import DeploymentRunner
from dog_rl_deploy.envs.lcm_agent import LCMAgent
from dog_rl_deploy.utils.cheetah_state_estimator import StateEstimator
from dog_rl_deploy.utils.command_profile import *

import pathlib

lc = lcm.LCM("udpm://239.255.76.67:7667?ttl=255")

def load_and_run_policy(label, experiment_name, max_vel=1.0, max_yaw_vel=1.0, max_vel_probe=1.0):
    # load agent
    dirs = glob.glob(f"../../legged_gym/logs/{label}/*") # TODO
    logdir = sorted(dirs)[0]
    print(logdir)

    with open(logdir+"/parameters.pkl", 'rb') as file:
        pkl_cfg = pkl.load(file)
        print(pkl_cfg.keys())
        cfg = pkl_cfg["Cfg"] # TODO
        print(cfg.keys())

    print('Config successfully loaded!')

    se = StateEstimator(lc)

    control_dt = 0.02
    command_profile = RCControllerProfile(dt=control_dt, state_estimator=se, x_scale=max_vel, y_scale=0.6, yaw_scale=max_yaw_vel, probe_vel_multiplier=(max_vel_probe / max_vel))

    hardware_agent = LCMAgent(cfg, se, command_profile)
    se.spin()

    from dog_rl_deploy.envs.history_wrapper import HistoryWrapper
    hardware_agent = HistoryWrapper(hardware_agent)
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

    deployment_runner.run(max_steps=max_steps, logging=True)

def reparameterize(mu, logvar):
    std = torch.exp(0.5 * logvar)
    eps = torch.randn_like(std)
    return eps * std + mu

def load_policy(logdir):
    actor = torch.jit.load(logdir + '/actor.pt').to('cuda:0')
    encoder = torch.jit.load(logdir + '/encoder.pt').to('cuda:0')
    vq_layer = torch.jit.load(logdir + '/vq_layer.pt').to('cuda:0')

    def policy(obs, info):
        encoding = encoder(obs["obs_history"].to('cuda:0'))
        z = vq_layer(encoding)
        action = actor(torch.cat((z, obs["obs"].to('cuda:0')), dim=-1)).to('cpu')
        info['z'] = z.to('cpu')
        return action

    return policy


if __name__ == '__main__':
    label = "a1_dreamwaq/exported"

    experiment_name = "a1_dreamwaq"

    load_and_run_policy(label, experiment_name=experiment_name, max_vel=3.0, max_yaw_vel=5.0, max_vel_probe=1.0)
