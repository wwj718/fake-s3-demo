#!/usr/bin/env python
# encoding: utf-8

'''
flask 本地文件服务

参考：http://docs.jinkan.org/docs/flask/patterns/fileuploads.html

gist：https://gist.github.com/dAnjou/2874714

flask.request.files.getlist("file[]")  上传多个文件

todo：
上传进度条  不该由后端 回复，前端自己知道  Upload Progress Bars
http://html5demos.com/dnd-upload
http://www.ruanyifeng.com/blog/2012/08/file_upload.html  # https://github.com/remy/html5demos/tree/master/demos
https://github.com/remy/html5demos/blob/master/demos/dnd-upload.html
'''

import os
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
import uuid

UPLOAD_FOLDER = '/tmp/'
#ALLOWED_EXTENSIONS = set(['txt','png'])
DENY_EXTENSIONS = set(['txt'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] not in DENY_EXTENSIONS

html_tpl = '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    <p>%s</p>
'''

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename) #移除中文，加uuid
            uuid_filename = "{}_{}".format(uuid.uuid4().get_hex()[:16],filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],uuid_filename))
            return redirect(url_for('index'))
    return html_tpl.format("<br>".join(os.listdir(app.config['UPLOAD_FOLDER'],)))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)



