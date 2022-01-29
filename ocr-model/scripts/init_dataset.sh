#!/bin/bash

cd "$(dirname "$0")" || exit 1

trdg --count 10 --language en --font ../data/font/OpenSans-Regular.ttf --format 32 --output_dir ../data/train