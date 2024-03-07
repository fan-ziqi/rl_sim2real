# rl_sim2real

[中文文档](README_CN.md)

## Connect to the Unitree Robot Dog

Connect to the robot dog's built-in wifi `UnitreeRoboticsA1-xxx`, test the connectivity

```bash
ping 192.168.123.12
```

If there is no problem, proceed to the next step

## Deploy Docker Environment

Go to the `scripts` folder under the root directory of this project and execute the deployment script. This script will download the Docker image and send it to the robot. (Password is 123)

```bash
cd rl_sim2real/scripts
bash deploy_env.sh
```

SSH into the robot

```
ssh unitree@192.168.123.12
```

Install Docker environment

```bash
cd ~/a1_gym/rl_sim2real/docker
bash unzip_image.sh
```

The above steps only need to be executed once

## Run the Controller

SSH into the robot

```bash
ssh unitree@192.168.123.12
```

Go to the `scripts` folder under the root directory of this project and run the `run_rl.sh` script. This script will stop the official Unitree process and run a custom lcm program with Docker

```bash
cd ~/a1_gym/rl_sim2real/scripts
bash run_rl.sh
```

Then press the LR key several times (about three or four times), and the dog will start moving.

**The left joystick controls xy, and the right joystick controls yaw**

Press the LR key again, and the dog will stop moving

This script will capture the exit signal, press Ctrl+C to automatically stop the program and kill related processes.

> Some code references https://github.com/Improbable-AI/walk-these-ways