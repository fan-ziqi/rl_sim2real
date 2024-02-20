#!/bin/bash
rsync -av --progress -e ssh --exclude=*.pt --exclude=*.mp4 --exclude=.git $PWD/../../../dog_rl_deploy $PWD/../../../legged_gym/logs/a1_blinddog/exported $PWD/../../setup.py unitree@192.168.123.12:/home/unitree/a1_gym
