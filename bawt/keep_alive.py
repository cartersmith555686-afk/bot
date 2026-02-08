from dashboard import app
from threading import Thread

def keep_alive():
    Thread(target=lambda: app.run(host="0.0.0.0", port=8080)).start()
