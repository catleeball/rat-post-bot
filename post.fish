#!/usr/bin/env fish

# This runs as a cron job:
#     0 8,20 * * *  fish post.fish

cd /home/cat/Services/RatPostBot
conda activate ratpostbot
python main.py &>> ratpostbot.log
