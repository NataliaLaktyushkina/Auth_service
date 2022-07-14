# gevent - чтобы сделать Flask асинхронным
from gevent import monkey
monkey.patch_all()  # заменяет все I/O-операции на асинхронные

from gevent.pywsgi import WSGIServer
import sys, os
sys.path.append(os.path.dirname(__file__) + '/..')
from auth_app import app_with_db

app = app_with_db()
http_server = WSGIServer(('', 5001), app)
http_server.serve_forever()
