#!/usr/bin/env python
# encoding: utf-8

# 写测试
from minio_client import MinioClient

# put: http://139.196.14.215:9000/mybucket/mytestkey?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=OIV5MPODN1Z2ID8R935X%2F20161027%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20161027T090214Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=da9cb4b528d331b656b79215202a4f79f3442387d142495179fa6ad4be9d6c28
# post : ('http://139.196.14.215:9000/mybucket/', {'x-amz-algorithm': 'AWS4-HMAC-SHA256', 'key': 'myobject', 'bucket': 'mybucket', 'x-amz-signature': '3e3a483b7bfe2d4db656417e198a146a12b8411856afcdaca4cc4abbd106578c', 'x-amz-date': '20161027T094240Z', 'policy': u'eyJleHBpcmF0aW9uIjoiMjAxNi0xMS0wNlQwOTo0Mjo0MC4wMDBaIiwiY29uZGl0aW9ucyI6W1siZXEiLCIkYnVja2V0IiwibXlidWNrZXQiXSxbInN0YXJ0cy13aXRoIiwiJGtleSIsIm15b2JqZWN0Il0sWyJlcSIsIiR4LWFtei1kYXRlIiwiMjAxNjEwMjdUMDk0MjQwWiJdLFsiZXEiLCIkeC1hbXotYWxnb3JpdGhtIiwiQVdTNC1ITUFDLVNIQTI1NiJdLFsiZXEiLCIkeC1hbXotY3JlZGVudGlhbCIsIk9JVjVNUE9ETjFaMklEOFI5MzVYLzIwMTYxMDI3L3VzLWVhc3QtMS9zMy9hd3M0X3JlcXVlc3QiXV19', 'x-amz-credential': 'OIV5MPODN1Z2ID8R935X/20161027/us-east-1/s3/aws4_request'})  # 前头是put 现在是post
# 上传一个文件 下载到本地/tmp


# 手动测试  httpie
