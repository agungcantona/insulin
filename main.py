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

app = Flask(__name__)
CLOUD_STORAGE_BUCKET = os.environ.get("CLOUD_STORAGE_BUCKET")

#saving links for affiliation & article
link_affiliation = 'https://insul-in-default-rtdb.firebaseio.com/affiliation_product.json'
link_article = 'https://insul-in-default-rtdb.firebaseio.com/article.json'

@app.route('/')
def homepage():

    # if request POST
    if request.method == 'POST':

        # parse variables & inputing it to an object called userData
        userData ={}
        userData["age"] = request.form.get('age')
        userData["gender"] = request.form.get('gender')
        userData["polyuria"] = request.form.get('polyuria')
        userData["polydipsia"] = request.form.get('polydipsia')
        userData["weight_loss"] = request.form.get('weight_loss')
        userData["weakness"] = request.form.get('weakness')
        userData["polyphagia"] = request.form.get('polyphagia')
        userData["genital_thrus"] = request.form.get('genital_thrus')
        userData["itching"] = request.form.get('itching')
        userData["irritability"] = request.form.get('irritability')
        userData["delayed_healing"] = request.form.get('delayed_healing')
        userData["partial_paresis"] = request.form.get('partial_paresis')
        userData["muscle_stiffness"] = request.form.get('muscle_stiffness')
        userData["alopecia"] = request.form.get('alopecia')
        userData["obesity"] = request.form.get('obesity')

        json_user = json.dumps(userData)
        json_loadUser= json.loads(json_user)

        if json_loadUser["result_diagnose"] == False:

            #reading data from url
            with urllib.request.urlopen(link_article) as url:
                article = json.loads(url.read().decode())
                i = list(range(3))
                x = {}
                x["article"] = random.sample(article, len(i))
                
                #merge
                merged_result = { **json_loadUser, **x}
                result= json.dumps(merged_result)
                final_result= json.loads(result)
                return final_result

        elif json_loadUser["result_diagnose"] == True:

            #reading data from url
            with urllib.request.urlopen(link_affiliation) as url:
                affiliation = json.loads(url.read().decode())
                i = list(range(3))
                x = {}
                x["affiliation_product"] = random.sample(affiliation, len(i))
                
                #merge
                merged_result = { **json_loadUser, **x}
                result= json.dumps(merged_result)
                final_result= json.loads(result)
                return final_result
        
    #if not POST
    userData ={
            "result_diagnose": bool(random.getrandbits(1)),
            "error": bool(1),
            "message": "method not supported"
        }

    json_user = json.dumps(userData)
    json_loadUser= json.loads(json_user)

    if json_loadUser["result_diagnose"] == False:

        #reading data from url
        with urllib.request.urlopen(link_article) as url:
            article = json.loads(url.read().decode())
            i = list(range(3))
            x = {}
            x["article"] = random.sample(article, len(i))

            #merge
            merged_result = { **json_loadUser, **x}
            result= json.dumps(merged_result)
            final_result= json.loads(result)
            return final_result

    elif json_loadUser["result_diagnose"] == True:

        #reading data from url
        with urllib.request.urlopen(link_affiliation) as url:
            affiliation = json.loads(url.read().decode())
            i = list(range(3))
            x = {}
            x["affiliation_product"] = random.sample(affiliation, len(i))

            #merge
            merged_result = { **json_loadUser, **x}
            result= json.dumps(merged_result)
            final_result= json.loads(result)
            return final_result


# If server error
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
    app.run(host="127.0.0.1", port=8080, debug=True)
