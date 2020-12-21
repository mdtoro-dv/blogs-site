#!/bin/bash
echo Starting web-site
cd /home/ubuntu/web-site
source env/Scripts/activate
gunicorn -b 0.0.0.0:443 --certfile=certificate.crt --keyfile=grupoeuninorte.pem wsgi:app
