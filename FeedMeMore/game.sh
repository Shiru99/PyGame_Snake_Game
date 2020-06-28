#!/usr/bin/env bash
x=$0
y=${x%/*}
# echo "$y"
# echo "$y/snake.py"

# cd /home/shiru/🃏\ Start/Python/PyGames/FeedMeMore && python3 /home/shiru/🃏\ Start/Python/PyGames/FeedMeMore/snake.py
cd "$y"
python3 "$y/snake.py"