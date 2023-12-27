#!/bin/bash
# download docker image if it doesn't exist yet
wget --directory-prefix=../docker -nc --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1XkVpyYyYqQQ4FcgLIDUxg-GR1WI89-XC' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1XkVpyYyYqQQ4FcgLIDUxg-GR1WI89-XC" -O ../../docker/deployment_image.tar && rm -rf /tmp/cookies.txt
