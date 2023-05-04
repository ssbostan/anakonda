bind = "0.0.0.0:8080"
wsgi_app = "anakonda:create_app()"
workers = 2
accesslog = "-"
errorlog = "-"
