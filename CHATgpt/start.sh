#!/bin/bash
export GOOGLE_CHROME_BIN=/usr/bin/google-chrome
gunicorn app:app
