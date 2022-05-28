from crypt import methods
from datetime import datetime

import logging
import os
import json
import random
import urllib.request

from flask import Flask, redirect, render_template, request

# from google.cloud import datastore
# from google.cloud import storage
# from google.cloud import vision

# CLOUD_STORAGE_BUCKET = os.environ.get("CLOUD_STORAGE_BUCKET")

app = Flask(__name__)


#saving links for affiliation & article
link_affiliation = 'https://insul-in-default-rtdb.firebaseio.com/affiliation_product.json'
link_article = 'https://insul-in-default-rtdb.firebaseio.com/article.json'

@app.route('/', methods=['GET', 'POST'])
def homepage():

    # if request POST
    if request.method == 'POST':

        # parse variables & inputing it to an object called userData
        userData ={
            "result_diagnose": bool(random.getrandbits(1)),
            "error": bool(0),
            "message": "success", 
            "user_info" : {
                "age" : request.form.get('age'),
                "gender" : request.form.get('gender'),
                "polyuria" : request.form.get('polyuria'),
                "polydipsia" : request.form.get('polydipsia'),
                "weight_loss" : request.form.get('weight_loss'),
                "weakness" : request.form.get('weakness'),
                "polyphagia" : request.form.get('polyphagia'),
                "genital_thrus" : request.form.get('genital_thrus'),
                "itching" : request.form.get('itching'),
                "irritability" : request.form.get('irritability'),
                "delayed_healing" : request.form.get('delayed_healing'),
                "partial_paresis" : request.form.get('partial_paresis'),
                "muscle_stiffness" : request.form.get('muscle_stiffness'),
                "alopecia" : request.form.get('alopecia'),
                "obesity" : request.form.get('obesity')
            }
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
        
    #if not POST
    elif request.method == 'GET':
        userData ={
                "result_diagnose": bool(random.getrandbits(1)),
                "error": bool(1),
                "message": "method not supported"
            }
        return userData

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
