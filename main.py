from datetime import datetime
import logging
import os
import json
import random
import urllib.request

from flask import Flask, redirect, render_template, request

from google.cloud import datastore
from google.cloud import storage
from google.cloud import vision


CLOUD_STORAGE_BUCKET = os.environ.get("CLOUD_STORAGE_BUCKET")


app = Flask(__name__)
link_affiliation = 'https://insul-in-default-rtdb.firebaseio.com/affiliation_product.json'
link_article = 'https://insul-in-default-rtdb.firebaseio.com/article.json'

@app.route("/")
def homepage():
    userData ={
        "result_diagnose":bool(random.getrandbits(1)),
        "error":bool(0),
        "message":"success"
    }

    json_user = json.dumps(userData)
    json_loadUser= json.loads(json_user)

    if json_loadUser["result_diagnose"] == False:

        #reading data from url
        with urllib.request.urlopen(link_article) as url:
            article = json.loads(url.read().decode())
            i = list(range(3))
            article_list = [article[0], article[1], article[2], article[3], article[4]]
            x = {}
            x["article"] = random.sample(article_list, len(i))
            merged_result = { **json_loadUser, **x}
            result= json.dumps(merged_result)
            final_result= json.loads(result)
            return final_result

    elif json_loadUser["result_diagnose"] == True:

        #reading data from url
        with urllib.request.urlopen(link_affiliation) as url:
            affiliation = json.loads(url.read().decode())
            i = list(range(3))
            affiliation_list = [affiliation[0], affiliation[1], affiliation[2], affiliation[3], affiliation[4], affiliation[5]]
            x = {}
            x["affiliation_product"] = random.sample(affiliation_list, len(i))
            merged_result = { **json_loadUser, **x}
            result= json.dumps(merged_result)
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
