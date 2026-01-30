import base64
import json
import logging
from flask import Flask, request, make_response

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

@app.route("/", methods=["POST"])
def gcs_event_handler():
    """
    Entry point for Pub/Sub PUSH messages coming from GCS notifications.
    """

    envelope = request.get_json(silent=True)

    if not envelope or "message" not in envelope:
        logging.error("Invalid Pub/Sub message format")
        return make_response("Bad Request", 400)

    pubsub_message = envelope["message"]

    # Decode Pub/Sub data (base64)
    if "data" in pubsub_message:
        data = base64.b64decode(pubsub_message["data"]).decode("utf-8")
        logging.info("Decoded Pub/Sub data: %s", data)

    attributes = pubsub_message.get("attributes", {})
    bucket_name = attributes.get("bucketId")
    object_name = attributes.get("objectId")

    logging.info("Received file event")
    logging.info("Bucket: %s", bucket_name)
    logging.info("Object: %s", object_name)

    return make_response("OK", 200)
