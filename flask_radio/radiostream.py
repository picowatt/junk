import flask
from flask import Response
import time
import socket
import sys
import threading

app = flask.Flask(__name__)

@app.route('/')
def main():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <title>ogg audio stream</title>
    </head>
    <body>
        <audio controls>
            <source src="/radio.ogg" type="audio/ogg" >
        </audio>
    </body>
    </html>
    """

@app.route('/radio.ogg')
def stream_ogg():
    def radio_ogg(socket):
        try:
            start = time.time()
            data = socket.recv(4096) 
            while (time.time() - start < 20):
                yield data
                data = socket.recv(4096)
        except:
            pass
        print("closing...", file=sys.stdout)
        socket.close()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", 6789))

    return Response(radio_ogg(sock), mimetype="audio/ogg")

app.run(host='0.0.0.0')