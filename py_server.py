#!/usr/bin/env python
# encoding: utf-8

#http://127.0.0.1:9000
# uuid
from minio import Minio
from minio.error import ResponseError
from datetime import timedelta

minio_server = "127.0.0.1:9000"
access_key = "OIV5MPODN1Z2ID8R935X"
secret_key = "rHJJn3kyhtnTs9c7VjeMU72Cf1X+ntoM36adWU3I"
region = "us-east-1"


# 写一个类
minioClient = Minio( minio_server,
                  access_key= access_key,
                  secret_key = secret_key,
                  secure=False)

def create_or_get_bucket(bucket_name):

    try:
        minioClient.make_bucket(bucket_name, location='us-east-1')
    except ResponseError as err:
        print(err)

# presigned Put object URL for an object name, expires in 3 days.
create_or_get_bucket("mybucket")

try:
        print(minioClient.presigned_put_object('mybucket',  # 默认是没有仓库的，初始化要创建
                                                  'myobject',
                                                  expires=timedelta(days=3)))
        # Response error is still possible since internally presigned does get
        # bucket location.
except ResponseError as err:
        print(err)
