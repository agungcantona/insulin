from datetime import datetime
import logging
import os
import json
import random
import pyrebase


from flask import Flask, redirect, render_template, request

from google.cloud import datastore
from google.cloud import storage
from google.cloud import vision


CLOUD_STORAGE_BUCKET = os.environ.get("CLOUD_STORAGE_BUCKET")


app = Flask(__name__)

#connect to db
config = {
    "apiKey": "AIzaSyAU91eIFsRIXmCNa3i7p3QltIy8WahvR-w",
    "authDomain": "capstone-project-test-7c88a.firebaseapp.com",
    "projectId": "capstone-project-test-7c88a",
    "storageBucket": "capstone-project-test-7c88a.appspot.com",
    "messagingSenderId": "844740250387",
    "appId": "1:844740250387:web:52dda9bbae8fbcd163a8e6",
    "measurementId": "G-RPZKSP3TGV",
    "databaseURL":"https://capstone-project-test-7c88a-default-rtdb.asia-southeast1.firebasedatabase.app/"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()

@app.route("/")
def homepage():
    userData ={
        "result_diagnose":bool(random.getrandbits(1)),
        "error":bool(random.getrandbits(1)),
        "message":random.choice(["success", "unauthorized"])
    }

    json_user = json.dumps(userData)
    json_loadUser= json.loads(json_user)

    if json_loadUser["result_diagnose"] == False:
        #reading data from DB
        json_article = db.child("Article").get()

        merged_result = { **json_loadUser, **json_article.val()}
        result= json.dumps(merged_result, sort_keys=False)
        final_result= json.loads(result)

        return final_result

    elif json_loadUser["result_diagnose"] == True:
        json_affiliation_product = db.child("Affiliation Product").get()

        merged_result = { **json_loadUser, **json_affiliation_product.val()}
        result= json.dumps(merged_result, sort_keys=False)
        final_result= json.loads(result)

        return final_result

@app.errorhandler(500)
def server_error(e):
    logging.exception("An error occurred during a request.")
    return (
        """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(
            e
        ),
        500,
    )

if __name__ == "__main__":
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host="127.0.0.1", port=8080, debug=True)
