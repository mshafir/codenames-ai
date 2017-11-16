cd frontend
ember build --environment=production
scp -r dist $1:~/web
# gunicorn server:app -b 127.0.0.1:5000 -w 4
