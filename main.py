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

#saving links for affiliation & article
link_affiliation = 'https://insul-in-default-rtdb.firebaseio.com/affiliation_product.json?limitToLast=3&orderBy=%22$key%22'
link_article = 'https://insul-in-default-rtdb.firebaseio.com/article.json?limitToLast=3&orderBy=%22$key%22'

@app.route('/', methods=['GET', 'POST'])
def homepage():

    # if request POST
    if request.method == 'POST':

        # parse variable
        age = request.form.get('age')
        gender = request.form.get('gender')
        polyuria = request.form.get('polyuria')
        polydipsia = request.form.get('polydipsia')
        weightLoss = request.form.get('weightLoss')
        weakness = request.form.get('weightness')
        polyphagia = request.form.get('polyphagia')
        genital_thrus = request.form.get('genital_thrus')
        itching = request.form.get('itching')
        irritability = request.form.get('irritability')
        delayed_healing = request.form.get('delayed_healing')
        partial_paresis = request.form.get('partial_paresis')
        muscle_stiffness = request.form.get('muscle_stiffness')
        alopecia = request.form.get('alopecia')
        obesity = request.form.get('obesity')

        #inputing data to an object called userData
        userData ={}
        userData["age"] = age
        userData["gender"] = gender
        userData["polyuria"] = polyuria
        userData["polydipsia"] = polydipsia
        userData["weightLoss"] = weightLoss
        userData["weakness"] = weakness
        userData["polyphagia"] = polyphagia
        userData["genital_thrus"] = genital_thrus
        userData["itching"] = itching
        userData["irritability"] = irritability
        userData["delayed_healing"] = delayed_healing
        userData["partial_paresis"] = partial_paresis
        userData["muscle_stiffness"] = muscle_stiffness
        userData["alopecia"] = alopecia
        userData["obesity"] = obesity

        json_user = json.dumps(userData)
        json_loadUser= json.loads(json_user)

        if json_loadUser["result_diagnose"] == False:

            #reading data from url
            with urllib.request.urlopen(link_article) as url:
                article = json.loads(url.read().decode())

                #Creating affiliation list
                x = {}
                x["article"] = article

                #merge result
                merged_result = { **json_loadUser, **x}
                result= json.dumps(merged_result)
                final_result= json.loads(result)
                return final_result

        elif json_loadUser["result_diagnose"] == True:

            #reading data from url
            with urllib.request.urlopen(link_affiliation) as url:
                affiliation = json.loads(url.read().decode())

                #Creating affiliation list
                x = {}
                x["affiliation_product"] = affiliation

                #merge result
                merged_result = { **json_loadUser, **x}
                result= json.dumps(merged_result)
                final_result= json.loads(result)
                return final_result
    
    #if not POST
    userData ={
            "result_diagnose": bool(random.getrandbits(1)),
            "error": bool(0),
            "message": "success"
        }

    json_user = json.dumps(userData)
    json_loadUser= json.loads(json_user)

    if json_loadUser["result_diagnose"] == False:

        #reading data from url
        with urllib.request.urlopen(link_article) as url:
            article = json.loads(url.read().decode())

            #Creating affiliation list
            x = {}
            x["article"] = article

            #merge result
            merged_result = { **json_loadUser, **x}
            result= json.dumps(merged_result)
            final_result= json.loads(result)
            return final_result

    elif json_loadUser["result_diagnose"] == True:

        #reading data from url
        with urllib.request.urlopen(link_affiliation) as url:
            affiliation = json.loads(url.read().decode())

            #Creating affiliation list
            x = {}
            x["affiliation_product"] = affiliation

            #merge result
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
