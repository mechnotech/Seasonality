#!/bin/bash
alembic upgrade head
cd src
python3 csv_to_db.py
python3 pywsgi.py

