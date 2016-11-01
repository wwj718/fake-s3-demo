#!/usr/bin/env python
# encoding: utf-8

#http://127.0.0.1:9000
# uui#!/usr/bin/env python
from __future__ import unicode_literals
from minio import Minio
from minio.error import ResponseError
from datetime import datetime, timedelta
from minio import PostPolicy

import time
# web server
import flask
#import mimetypes
import json
from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
app = Flask(__name__)
CORS(app)

#minio_server = "127.0.0.1:9000"
MINIO_SERVER = "139.196.14.215:9000"
ACCESS_KEY = "OIV5MPODN1Z2ID8R935X"
SECRET_KEY = "rHJJn3kyhtnTs9c7VjeMU72Cf1X+ntoM36adWU3I"
REGION = "us-east-1"


# todo  上传后，nginx观看
# from minio import PostPolicy  设置控制项目
# 如何获得文件名  七牛是在callback里有，存下的时候有文件类型 文件名
# 使用notification机制: https://docs.minio.io/docs/python-client-api-reference#get_bucket_notification
# 解决！ 去后台请求key的时候就需要把信息带过去
# 测试驱动
# 使用requests/httpie测试
class MinioClient(object):
    """minit client"""

    def __init__(self, bucket_name):
        """TODO: to be defined1. """
        self.client = Minio(MINIO_SERVER,
                            access_key=ACCESS_KEY,
                            secret_key=SECRET_KEY,
                            secure=False)
        self.bucket_name = bucket_name

    def create_or_get_bucket(self,bucket_name):

        try:
            self.client.make_bucket(self.bucket_name, location=REGION)
        except ResponseError as err:
            print(err) #显示错误不退出程序

    # Key = test
    # 文件类型和后缀无关
    # 文件名是怎么决定，key+文件名 看七牛的实现
    def get_presigned_put_url(self,key,time_delta=60):  # key uuid
        try:
            url  = self.client.presigned_put_object(self.bucket_name,  # 默认是没有仓库的，初始化要创建
                                                          key,
                                                          expires=timedelta(minutes=time_delta)) # 默认一小时  Expiry in seconds. Default expiry is set to 7 days
            #print(url)
            return url
        # Response error is still possible since internally presigned does get
        except ResponseError as err:
            print(err)

    def get_presigned_post_url(self):
        post_policy = PostPolicy()
        # Apply upload policy restrictions:
        # set bucket name location for uploads.
        post_policy.set_bucket_name(self.bucket_name,)
        # set key prefix for all incoming uploads.
        post_policy.set_key_startswith('myobject') #为何成为名字了,文件名没了
        # set content length for incoming uploads.
        #post_policy.set_content_length_range(10, 1024)
        # set expiry 10 days into future.
        expires_date = datetime.utcnow()+timedelta(days=10)
        post_policy.set_expires(expires_date)
        try:
            signed_form_data = self.client.presigned_post_policy(post_policy)
            return signed_form_data
        except ResponseError as err:
            print(err)


    def format4httpie(self,signed_form_data):
        # 这部分可以用ajax
        http_str = 'http --form POST {0}'.format(signed_form_data[0]) # # url
        http_cmd = [http_str]
        for field in signed_form_data[1]: # 是个字典
            http_cmd.append(' {0}={1}'.format(field, signed_form_data[1][field]))

        # print curl command to upload files.
        http_cmd.append(' file=@<FILE>')

        return ' '.join(http_cmd)


def main():
    bucket_name = "mybucket"
    client = MinioClient(bucket_name)
    put_url = client.get_presigned_put_url(key="mytestkey")
    #signed_form_data = client.get_presigned_post_url()
    print(put_url)
    #commmand =  client.format4httpie(signed_form_data)
    #print(commmand)  # 如何变为js也能上传

@app.route('/get_put_url',methods=["GET",'POST'])
def get_put_url():
    object_name = request.args.get('objectName') #中文 url化
    #content_type = mimetypes.guess_type(object_name)[0]

    bucket_name = "mybucket"
    client = MinioClient(bucket_name)
    put_url = client.get_presigned_put_url(key="test") #不能有点号？
    print(put_url)
    time.sleep(5) #为了要延时  诡异的bug  单进程的原因？ 之前的为也是这个引起？
    return flask.jsonify({'url':put_url}) #中文
    #print(put_url)





if __name__ == '__main__':
    #main()
    #app.run(host='0.0.0.0',port='5000',processes=2)
    app.run()
