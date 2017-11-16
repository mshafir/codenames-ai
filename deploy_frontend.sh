cd frontend
ember build --environment=production
scp -rf dist/* $1:~/web
