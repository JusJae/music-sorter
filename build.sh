#!usr/bin/env bash
# Exit on error
set -e  errexit

# Install dependencies
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --noinput

# Apply database migrations
python manage.py migrate