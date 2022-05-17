from datetime import datetime
import logging
import os
import json
import random


from flask import Flask, redirect, render_template, request

from google.cloud import datastore
from google.cloud import storage
from google.cloud import vision


CLOUD_STORAGE_BUCKET = os.environ.get("CLOUD_STORAGE_BUCKET")


app = Flask(__name__)

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
        json_article ={
        	"article":{
              "id_article_1":{
                  "article_title": "Diabetes penyakit serius",
                  "article_image_url": "url",
                  "article_provider_name": "Liputan6.com",
                  "article_url": "some url to article"
              },
              "id_article_2":{
                  "article_title": "Diabetes penyakit serius",
                  "article_image_url": "url",
                  "article_provider_name": "Liputan6.com",
                  "article_url": "some url to article"
              },
              "id_article_3":{
                  "article_title": "Diabetes penyakit serius",
                  "article_image_url": "url",
                  "article_provider_name": "Liputan6.com",
                  "article_url": "some url to article"
              }
            }
        }

        json_res=json.dumps(json_article)
        json_result=json.loads(json_res)
        merged_result = { **json_loadUser, **json_result}
        result= json.dumps(merged_result, sort_keys=False)
        final_result= json.loads(result)
        return final_result

    elif json_loadUser["result_diagnose"] == True:
        json_affiliation_product ={
        	"affiliation_product":{
              "affiliation_id_1":{
                  "product_url": "some url",
                  "product_name": "Insulin sehat",
                  "product_image_url": "url image",
                  "product_price": 50000,
                  "product_store_image_url": "url"
              },
              "affiliation_id_2":{
                  "product_url": "some url",
                  "product_name": "Insulin sehat",
                  "product_image_url": "url image",
                  "product_price": 60000,
                  "product_store_image_url": "url"
              },
              "affiliation_id_3":{
                  "product_url": "some url",
                  "product_name": "Insulin sehat",
                  "product_image_url": "url image",
                  "product_price": 70000,
                  "product_store_image_url": "url"
              }
            }
        }

        json_res= json.dumps(json_affiliation_product)
        json_result= json.loads(json_res)
        merged_result = { **json_loadUser, **json_result}
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
