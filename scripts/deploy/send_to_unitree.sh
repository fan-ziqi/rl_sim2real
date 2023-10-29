#!/bin/bash
rsync -av -e ssh --exclude=*.pt --exclude=*.mp4 $PWD/../../a1_gym_deploy $PWD/../../runs $PWD/../setup.py unitree@192.168.123.12:/home/unitree/a1_gym
