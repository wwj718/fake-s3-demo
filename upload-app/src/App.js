import React, { Component } from 'react';
//npm install superagent
var request = require('superagent');
import logo from './logo.svg';
import './App.css';
//import { ReactS3Uploader } from 'react-s3-uploader';
//var ReactS3Uploader = require('react-s3-uploader');


//upload compoment
//https://github.com/FineUploader/react-fine-uploader
//http://docs.fineuploader.com/branch/master/quickstart/03-setting_up_server.html
//endpoint  是变化的非常麻烦
//import FineUploaderTraditional from 'react-fine-uploader'
//import Gallery from 'react-fine-uploader/components/gallery'
//import FineUploaderS3 from 'react-fine-uploader/wrappers/s3'


// fetch 回调的风格来写  转态的变化  每当变化才上传
//var put_url = "http://139.196.14.215:9000/mybucket/test.txt?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Expires=3600&X-Amz-Credential=OIV5MPODN1Z2ID8R935X%2F20161101%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-SignedHeaders=host&X-Amz-Date=20161101T020908Z&X-Amz-Signature=0832716fc7f49d5084259d7af6f0072d9612e90bcf0e879c92ea4ad2a92b987b" //上传的瞬间才获得上传的地址

//整个这个是变化的，组件中需要处理这个变化 state  如何处理变化
// 直传
// 经典上传对后端有要求，无法使用
/*
const uploader = new FineUploaderTraditional({
    options: {
        chunking: {
            enabled: true
        },
        deleteFile: {
            enabled: true,
            endpoint: put_url //是个函数就行 ，不会等待返回的  这个需求太常见了, url  signature
        },
        request: {
            endpoint: put_url //this.pros.put_url
        }, //回调生成 有一个网络请求的过程 s3都有  不会处理转态  准备上传时限请求,改变状态
        retry: {
            enableAuto: true
        }
    }
})
*/

/*
const uploader = new FineUploaderS3({
    options: {
        request: {
            endpoint: "http://139.196.14.215:9000/minio",
            accessKey: "OIV5MPODN1Z2ID8R935X"
        },
        signature: {
            endpoint: "http://127.0.0.1:5000/get_put_url"
        }
    }
})
*/


var Dropzone = require('react-dropzone');



function retrieveNewURL(file, callback)
    { //cb: callback 基于事件，何时回来呢
        //可以先本地跑起来服务，flask跑起来 , 之后翻译为django
        const params = {
            objectName: file.name,
            contentType: file.type
        };
        var presignUrl = "http://127.0.0.1:5000/get_put_url"
        //fetch
        var req = request.get(presignUrl);
        req.query(params);//http://visionmedia.github.io/superagent/#get-requests
        req.end(function(err, res){
        // Calling the end function will send the request
          //
           var url = res.body['url']
           console.log("retrieveNewURL",res.body['url']);
           callback(url);
        })

  }


function uploadFile(file, url)
    {
        let data = new FormData();
        data.append(file.name, file)
        console.log(url);
        //使用request
        fetch(url,
        {
            method: 'PUT',
            body: data,
        })
    }


var DropzoneDemo = React.createClass({
    getInitialState: function () {
        return {
          files: []
        };
    },

    /*
    onDrop: function (acceptedFiles) {
      this.setState({
        files: acceptedFiles //变化
      });
    },
    */
    onDrop: function(acceptedFiles){
        //https://github.com/visionmedia/superagent request
        //retrieveNewURL
        //var req = request.post('/upload');
        acceptedFiles.forEach((file)=> {
          //先get变化的url
          retrieveNewURL(file, (url) =>
                {
                    uploadFile(file, url)
                })
            //req.attach(file.name, file);
        });
        //req.end(callback);
    },

    onOpenClick: function () {
      this.dropzone.open();
    },

    render: function () {
        return (
            <div>
                <Dropzone ref={(node) => { this.dropzone = node; }} onDrop={this.onDrop}>
                    <div>Try dropping some files here, or click to select files to upload.</div>
                </Dropzone>
                <button type="button" onClick={this.onOpenClick}>
                    Open Dropzone
                </button>
                {this.state.files.length > 0 ? <div>
                <h2>Uploading {this.state.files.length} files...</h2>
                <div>{this.state.files.map((file) => <img src={file.preview} /> )}</div>
                </div> : null}
            </div>
        );
    }
});


/*
class UploadComponent extends Component {
    render() {
        return (
            <Gallery uploader={ uploader } />
        )
    }
}
*/

//export default UploadComponent


//布局也在app里做 app是应用的概念 一个页面可以视为一个应用
class App extends Component {
  render() {
    return (
      <div className="App">
        <div className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h2>Welcome to React</h2>
        </div>
        <p className="App-intro">
          To get started, edit <code>src/App.js</code> and save to reload.
          ok
        </p>
        {/*记得加大括号,多行注释也是这个
         signingUrl是啥
         <ReactS3Uploader
    signingUrl="/get_put_url"
    accept="image/*"
    preprocess={this.onUploadStart}
    onProgress={this.onUploadProgress}
    onError={this.onUploadError}
    onFinish={this.onUploadFinish}
    signingUrlHeaders={{ additional: "headers" }}
    signingUrlQueryParams={{ additional: "query-params" }}
    uploadRequestHeaders={{ 'x-amz-acl': 'public-read' }}
    contentDisposition="auto"
    server="http://127.0.0.1:5000" />
          */}
         <DropzoneDemo />
      </div>
    );
  }
}

export default App;
