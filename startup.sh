#!/bin/bash
python -m pip install -r requirements.txt
gunicorn --bind=0.0.0.0:8000 agrosmart_backend.wsgi:application