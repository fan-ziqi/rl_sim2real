#!/bin/bash
rsync -av --progress -e ssh --exclude=*.pt --exclude=*.mp4 --exclude=.git $PWD/../../../dog_rl_deploy $PWD/../../../runs $PWD/../../setup.py unitree@192.168.123.12:/home/unitree/a1_gym
