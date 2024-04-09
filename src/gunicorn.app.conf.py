wsgi_app = 'ProjetDjango1.wsgi:application'
bind = 'unix:/tmp/gunicorn/gunicorn-app.sock'
worker_class = 'sync' # default
worker = 4
accesslog = '-'
