#!/bin/bash

nohup python ./scripts/server_8000.py &
nohup python ./scripts/admin_bot.py &
nohup python routes.py
