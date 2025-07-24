#!/bin/bash
export GOOGLE_CHROME_BIN=/usr/bin/google-chrome
gunicorn app:app --timeout 120 -b 0.0.0.0:$PORT
