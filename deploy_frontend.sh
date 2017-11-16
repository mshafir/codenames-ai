cd frontend
ember build --environment=production
scp -r dist/* $1:~/web
