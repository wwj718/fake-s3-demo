#!/usr/bin/env python
# encoding: utf-8

# 依赖 ： boto3,flask,flask_cors

import sys;reload(sys);sys.setdefaultencoding('utf8')
import boto3
from botocore.client import Config
import requests
import uuid

import flask
import mimetypes
import json
from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
app = Flask(__name__)
CORS(app)


'''
直接支持cas，完全独立，支持统一身份,不依赖在任何app里
'''

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



@app.route('/get_put_url',methods=["GET",'POST'])
def get_put_url():
    object_name = request.args.get('objectName').decode("utf-8") # uuid,之后可以把username加进来
    uuid_object_name = "{}_{}".format(uuid.uuid4().get_hex()[:16] , object_name) # 中文问题 ,使用sys.setdefaultencoding解决!
    # todo : 存到本地 ， 然后增加删除功能
    #content_type = mimetypes.guess_type(object_name)[0]
    bucket_name = "mybucket"

    url = s3.generate_presigned_url(
    ClientMethod='put_object',
    # ACL, Body, Bucket, CacheControl, ContentDisposition, ContentEncoding, ContentLanguage, ContentLength, ContentMD5, ContentType, Expires, GrantFullControl, GrantRead, GrantReadACP, GrantWriteACP, Key, Metadata, ServerSideEncryption, StorageClass, WebsiteRedirectLocation, SSECustomerAlgorithm, SSECustomerKey, SSECustomerKeyMD5, SSEKMSKeyId, RequestPayer
    Params={
        'Bucket': bucket_name,
        'Key': uuid_object_name,
        #'ContentType': content_type, #加上这个就有问题
        #'ACL': "public-read",
    },
    )
    #直接上传
    #requests.put(url, data=open("/tmp/test.txt").read())
    return flask.jsonify({"url":url})


# 写一个函数登录服务器通知
# https://docs.minio.io/docs/minio-client-complete-guide
# https://docs.minio.io/docs/python-client-api-reference#listen_bucket_notification  监控变化，通知
# 先假设上传就是到了服务器

@app.route('/get_object_list',methods=["GET"])  # 分页 用django很好实现
def get_object_list():
    bucket_name = "mybucket"
    # 直接列出，不要本地存储

    return flask.jsonify({'url':url})


@app.route('/delete/<object_uuid>',methods=["DELETE"])
def delete_object(object_uuid):
    '''
    删除：
        *  本地字段
        *  删除monio
    '''
    bucket_name = "mybucket"
    return flask.jsonify({'object_uuid':object_uuid}) #中文
    #print(put_url)





@app.route('/get_get_url',methods=["GET"]) # flask : send_from_directory
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
