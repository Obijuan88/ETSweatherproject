#!/bin/bash

# Start the cron service in the foreground
crond -f &

# Run the application
python src/telegrambot.py

# Keep the container running
tail -f /var/log/cron.log