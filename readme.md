# fake-s3 

构建仿s3的存储服务

for [openEduMedia](https://github.com/openEduClub/openEduMedia)

# 已有工作
*  [构建类s3存储系统（Minio）](http://blog.just4fun.site/install-Minio-Cloud-Storage.html)

# 组件
*  minio
    *  [Upload files from browser using pre-signed URLs](https://docs.minio.io/docs/upload-files-from-browser-using-pre-signed-urls)
    *  [RoR Resume Uploader App](https://docs.minio.io/docs/ror-resume-uploader-app)  使用aws
    *  [python client presigned_put_object](https://docs.minio.io/docs/python-client-api-reference#presigned_put_object)  无法用于上传


# minio
### 安装与启动

```bash
curl -O https://dl.minio.io/server/minio/release/linux-amd64/minio
chmod +x minio
./minio --help
mkdir ~/minio_test
./minio server ~/minio_test
```

### python client
作为后端 分发凭证,rest(crud)

```
pip install minio
```

# 前端
```
npm config set registry https://registry.npm.taobao.org #设置taobao源
npm install -g create-react-app
create-react-app upload-app
```

### start and build

```
cd upload-app
npm start # 开发
npm run build # 发布
```

build之后到upload-app/build目录下: `python -m SimpleHTTPServer 8000`



# 开发
我在mac下开发，对应的minio版本为[darwin-amd64/minio](https://dl.minio.io/server/minio/release/darwin-amd64/minio)


# 关于redux
暂时采用发布订阅模式（事件驱动）吧，可以模范kinto_admin来做
