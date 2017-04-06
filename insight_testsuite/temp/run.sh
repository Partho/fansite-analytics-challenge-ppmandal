#!/usr/bin/env bash

echo -e "\n Executing Feature 1"
python ./src/most_active_hosts.py ./log_input/log.txt ./log_output/hosts.txt

echo -e "\nExecuting Feature 2"
python ./src/most_bandwidth_consumers.py ./log_input/log.txt ./log_output/resources.txt

echo -e "\nExecuting Feature 3"
python ./src/most_busiest_hourwise.py ./log_input/log.txt ./log_output/hours.txt

echo -e "\nExecuting Feature 4"
python ./src/consecutive_failed_logins.py ./log_input/log.txt ./log_output/blocked.txt