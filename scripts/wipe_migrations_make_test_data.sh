#!/bin/bash

# Example script to delete the migrations directory for "core" app, delete the
# sqlite database, then recreate it, and setup test data
rm -r apps/core/migrations
rm bookclub/db.sqlite3
python manage.py makemigrations core
python manage.py migrate
python manage.py setup_test_bookclub_data

