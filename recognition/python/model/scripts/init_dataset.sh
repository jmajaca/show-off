#!/bin/bash

cd "$(dirname "$0")" || exit 1

echo 'Generating 60k words'
trdg --count 10000 --language en --font ../data/font/OpenSans-Regular.ttf --format 32 -k 5 -rk --output_dir ../data/train
trdg --count 10000 --language en --font ../data/font/Raleway-Regular.ttf --format 32 -k 5 -rk --output_dir ../data/train
trdg --count 10000 --language en --font ../data/font/Lato-Regular.ttf --format 32 -k 5 -rk --output_dir ../data/train
trdg --count 10000 --language en --font ../data/font/AmaticSC-Regular.ttf --format 32 -k 5 -rk --output_dir ../data/train
trdg --count 10000 --language en --font ../data/font/Aller-Regular.ttf --format 32 -k 5 -rk --output_dir ../data/train
trdg --count 10000 --language en --font ../data/font/Roboto-Regular.ttf --format 32 -k 5 -rk --output_dir ../data/train
# trdg -i ../data/words.txt --count 39996  --font ../data/font/OpenSans-Regular.ttf --format 32 --output_dir ../data/train

echo 'Removing words with special characters'
WORDS_TO_REMOVE=( $(ls ../data/train | grep -E "(['!?&$:-]|.*\..*\.jpg)") ) # special chars: '!?&$:-.
for file in "${WORDS_TO_REMOVE[@]}"
do
  rm "../data/train/$file"
done
echo "Removed ${#WORDS_TO_REMOVE[@]} words"

echo 'Move 10% of words to test set'
WORD_COUNT="$(ls ../data/train | wc -l)"
TEST_WORD_COUNT="$(bc <<< "$WORD_COUNT*0.1")"
TEST_WORD_COUNT=${TEST_WORD_COUNT::-2}
WORDS_TO_MOVE=( $(ls ../data/train | shuf -n "$TEST_WORD_COUNT") )
for file in "${WORDS_TO_MOVE[@]}"
do
  mv "../data/train/$file" ../data/test
done

echo 'All done'