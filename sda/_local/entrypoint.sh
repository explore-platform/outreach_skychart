#!/bin/bash
printf "====================================
BOOTING SDA
====================================
"
python3 /sda/DashApp.py
# gunicorn DashApp:server --reload -b 0.0.0.0:8050