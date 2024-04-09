wsgi_app = 'ProjetDjango1.asgi:application'
worker_class = 'uvicorn.workers.UvicornWorker'
#workers = 2

#Utilisation du nombre maximum de travailleurs possible
workers = 2

bind = 'unix:/tmp/gunicorn/gunicorn-channel.sock'
accesslog = '-'
