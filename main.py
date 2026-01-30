import base64
import json
import logging
from flask import Flask, request

#Just checking

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route("/", methods=["POST"])
def receive_event():
    envelope = request.get_json()

    if not envelope or "message" not in envelope:
        logging.error("Invalid Pub/Sub message format")
        return ("Bad Request", 400)

    pubsub_message = envelope["message"]

    if "data" in pubsub_message:
        data = base64.b64decode(pubsub_message["data"]).decode("utf-8")
        logging.info("Received message data: %s", data)
    else:
        logging.info("No data in message")

    return ("OK", 200)
