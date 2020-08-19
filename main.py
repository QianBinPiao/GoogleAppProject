from flask import Flask, url_for, jsonify, send_file, send_from_directory,flash
from flask import render_template
from flask import request, redirect
import os
import uuid
import base64
from werkzeug.utils import secure_filename
import logging
from google.cloud import storage
import tempfile

UPLOAD_FOLDER = 'static/'

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')




@app.route('/getResultImage', methods=['GET', 'POST'])
def getResultImage():
    storage_client = storage.Client()
    bucket = storage_client.get_bucket('project2_bucket_logs')
    blob_download = bucket.blob('image.png')
    with tempfile.NamedTemporaryFile() as temp:
        blob_download.download_to_filename(temp.name)
        #return send_file(filename_or_fp = temp.name, mimetype = 'image/png')
        return base64.b64encode(temp.read())

@app.route('/getResultMessage', methods=['GET', 'POST'])
def getResultMessage():
    destination = "static/image_result.txt"

    storage_client = storage.Client()
    bucket_name = "project2_bucket_logs"
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob("image_result.txt")
    #blob.download_to_filename(destination)
    destination_string = blob.download_as_string()

    return destination_string.decode('ascii')

@app.route('/startSignal', methods=['GET', 'POST'])
def startSignal():
    storage_client = storage.Client()
    bucket = storage_client.get_bucket('project2_bucket_logs')
    blob_text = bucket.blob('start.txt')
    blob_text.upload_from_string(data="1")
    return "success"

@app.route('/checkSignal', methods=['POST'])
def checkSignal():
    storage_client = storage.Client()
    bucket = storage_client.get_bucket('project2_bucket_logs')
    blob = bucket.blob('start.txt')
    destination_string = blob.download_as_string()

    return destination_string.decode('ascii')

@app.route('/getAccuracyImage', methods=['GET', 'POST'])
def getAccuracyImage():
    # os.environ.setdefault("GCLOUD_PROJECT", "project-kaiqi-test")
    # storage_client = storage.Client.from_service_account_json('./credentials.json')
    storage_client = storage.Client()
    bucket = storage_client.get_bucket('project2_bucket_logs')
    blob_download = bucket.blob('acc_figure.png')
    # blob_download.download_to_filename("./plot_acur/acc_figure.png")

    # graphFile = open("plot_acur/acc_figure.png", "r")
    with tempfile.NamedTemporaryFile() as temp:
        blob_download.download_to_filename(temp.name)
        #print(temp.name)

        #return send_file(filename_or_fp = temp.name, mimetype = 'image/png')
        return base64.b64encode(temp.read())


@app.route('/fileUpload', methods=['POST'])
def fileUpload():
    uploadedFile = request.files['file']
    print(type(uploadedFile))
    storage_client = storage.Client()
    bucket = storage_client.get_bucket('project2_bucket_logs')
    blob_upload= bucket.blob('image.png')
    blob_upload.upload_from_file(file_obj=uploadedFile, content_type="image/png")
    blob_text = bucket.blob('image.txt')
    blob_text.upload_from_string(data="1")
    return "success"


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
