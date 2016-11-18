#!/bin/bash

cd "$(dirname "$0")"

if [ ! -f 0.y4m ]; then
  wget https://s3-us-west-1.amazonaws.com/excamera-test-vectors/videochat/0.y4m
fi

if [ ! -f 1.y4m ]; then
  wget https://s3-us-west-1.amazonaws.com/excamera-test-vectors/videochat/1.y4m
fi
