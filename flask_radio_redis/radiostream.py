import flask
from flask import Response
import time
import sys
import redis

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
            <source src="/radio.mp3" type="audio/mpeg" >
        </audio>
    </body>
    </html>
    """

@app.route('/radio.mp3')
def stream_ogg():
    def radio_ogg(sub, rdb):
        r = rdb
        start = time.time()
        print("start", file=sys.stdout)
        while (time.time() - start < 30):
            msg = sub.get_message(timeout=2)
            if msg:
                data = msg['data']
                print(len(data), file=sys.stdout)
                yield data

    rdb = redis.StrictRedis(host='localhost', port=6379, db=0)
    sub = rdb.pubsub(ignore_subscribe_messages=True)
    sub.subscribe('radio')
    if(sub.get_message() == None):
        pass

    return Response(radio_ogg(sub, rdb), mimetype="audio/mpeg")

app.run(host='0.0.0.0')