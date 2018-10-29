#!/bin/bash

nohup python ./scripts/admin_bot.py &
nohup python routes.py &
nohup python ./scripts/server_8000.py 