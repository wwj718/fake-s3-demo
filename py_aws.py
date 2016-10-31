#!/usr/bin/env python
# encoding: utf-8
import boto3
from botocore.client import Config
import requests

import flask
#import mimetypes
import json
from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
app = Flask(__name__)
CORS(app)


# Get the service client.
minio_server = "http://139.196.14.215:9000"
access_key = "OIV5MPODN1Z2ID8R935X"
secret_key = "rHJJn3kyhtnTs9c7VjeMU72Cf1X+ntoM36adWU3I"
region = "us-east-1"
bucket = "mybucket"


s3 = boto3.client('s3',
                    endpoint_url=minio_server,
                    aws_access_key_id= access_key,
                    aws_secret_access_key= secret_key,
                    config=Config(signature_version='s3v4'),
                    region_name=region)


# Use the URL to perform the GET operation. You can use any method you like
# to send the GET, but we will use requests here to keep things simple.

@app.route('/get_put_url',methods=["GET",'POST'])
def get_put_url():
    object_name = request.args.get('objectName') #中文 url化
    #content_type = mimetypes.guess_type(object_name)[0]
    bucket_name = "mybucket"
    #time.sleep(5) #为了要延时  诡异的bug  单进程的原因？ 之前的为也是这个引起？

    url = s3.generate_presigned_url(
    ClientMethod='put_object',
    Params={
        'Bucket': bucket_name,
        'Key': object_name
    })

    return flask.jsonify({'url':url}) #中文
    #print(put_url)

@app.route('/get_get_url',methods=["GET"])
def get_get_url():
    bucket_name = "mybucket"
    url = s3.generate_presigned_url(
    ClientMethod='get_object',
    Params={
        'Bucket': bucket_name,
        'Key': "video_frequent_replays.png"
    })

    return flask.jsonify({'url':url}) #中文
    #print(put_url)





if __name__ == '__main__':
    #main()
    #app.run(host='0.0.0.0',port='5000',processes=2)
    app.run()
