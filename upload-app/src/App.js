import React, { Component } from 'react';

var request = require('superagent');//npm install superagent
import logo from './logo.svg';
import './App.css';
var Dropzone = require('react-dropzone');
//material-ui
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
//import MyAwesomeReactComponent from './MyAwesomeReactComponent';
import FloatingActionButton from 'material-ui/FloatingActionButton';
//import ContentAdd from 'material-ui/svg-icons/content/add';
import UploadIcon from 'material-ui/svg-icons/file/cloud-upload';



/*
 * kinto 使用一个类来维持转态，不用redux，传递到各个地方，监听和发布来处理事件
*/

//bar
//import LinearProgressExampleDeterminate from './linear_progress.js';
import LinearProgress from 'material-ui/LinearProgress';

//https://github.com/ruanyf/react-demos  学习demo
//https://github.com/ruanyf/react-demos#demo08-thisstate
/*
//redux
import { createStore, combineReducers } from 'redux'  //不要用黏合的，太他妈烦了

var itemsReducer = function (state = [], action) {
    console.log('itemsReducer was called with state', state, 'and action', action)

    switch (action.type) {
        case 'ADD_ITEM':
            return [
                ...state,
                action.item
            ]
        default:
            return state;
    }
}

var reducer = combineReducers({ items: itemsReducer })
var store_0 = c reateStore(reducer)

store_0.subscribe(function() {
    console.log('store_0 has been updated. Latest store state:', store_0.getState());
    // 在这里更新你的视图 , 如何更新
})

var addItemActionCreator = function (item) {
    return {
        type: 'ADD_ITEM',
        item: item
    }
}

store_0.dispatch(addItemActionCreator({ id: 1234, description: 'anything' }))
////////////////////redux
*/

function retrieveNewURL(file, callback)
    {   // callback 基于事件，何时回来呢
        //可以先本地跑起来服务，flask跑起来 , 之后翻译为django
        const params = {
            objectName: file.name,
            contentType: file.type
        };
        var presignUrl = "http://127.0.0.1:5000/get_put_url"
        var req = request.get(presignUrl);
        req.query(params);//http://visionmedia.github.io/superagent/#get-requests
        req.end(function(err, res){
        // Calling the end function will send the request
           var url = res.body['url']
           console.log("retrieveNewURL",res.body['url']);
           callback(url);
        })

  }


//正式上传
// 进度条 html5就能做到 : http://www.ruanyifeng.com/blog/2012/08/file_upload.html
// The best way to upload files, with progress events, is still using XHR directly rather than fetch
// http://stackoverflow.com/questions/28750489/upload-file-component-with-reactjs 终极

var DropzoneDemo = React.createClass({
    getInitialState: function () {
        return {
          files: [],
          completed:0,
        };
    },
    //内部不能写方法？ 外部去改变
    //辅助函数
    change_completed: function(value){
        this.setState({completed: value});
    }, //需要绑定到this吗

     uploadFile:function(file, url)
    //You have to bind your event handlers to correct context (this):
    //普通函数如何改写状态，只能发送信息，要求更改 ,action 发送事件
    //https://github.com/react-guide/redux-tutorial-cn
    {
        //this.setState({completed: 2});
        //console.log('uploadFile:fun ', this.state.completed,0); //在此有效
        let data = new FormData();
        data.append(file.name, file)
        console.log(url);
        //进度条    Upload Progress Bars
        //fetch 不支持进度条 需要用xhr
        var self = this; //把外部this存下来
        console.log("开始上传");
        var req = request.put(url)
        .set("Content-Type", "application/octet-stream") //移除webkit标识了
        .send(file)
        .on('progress',  function(e) {
    this.setState(function(state){
        console.log("progress",e.percent
)
        return {
          completed:e.percent,
        };
    });
}.bind(this))
        req.end(function(err, res){
           console.log("上传完成",res);
        }) },

    onDrop: function(acceptedFiles){
        //retrieveNewURL
        var topthis=this;
        //console.log('Percentage done: ', this.state.completed);
        this.setState({files: acceptedFiles});
        acceptedFiles.forEach((file)=> {
          //先get变化的url
          retrieveNewURL(file, (url) =>
                {
                    console.log(topthis);
                    this.uploadFile(file, url)
                })
            //req.attach(file.name, file);
        });
        //req.end(callback);
    },

    onOpenClick: function () {
      this.dropzone.open();
    },

    //ui
    render: function () {
        var completed = this.state.completed;
        return (
            <div>
                <Dropzone ref={(node) => { this.dropzone = node; }} onDrop={this.onDrop}>
                    <div>将文件拖曳到当前区域或者点击上传.</div>
                </Dropzone>
                <MuiThemeProvider>
                <LinearProgress mode="determinate" value={this.state.completed} />
                </MuiThemeProvider>
                <MuiThemeProvider>
                  <FloatingActionButton onClick={this.onOpenClick}>
                    <UploadIcon />
                  </FloatingActionButton>
                </MuiThemeProvider>

                {this.state.files.length > 0 ? <div>
                <h2>正在上传 {this.state.files.length}  个文件， 完成：{this.state.completed} %...</h2>
                <div>{this.state.files.map((file) => <img alt="" src={file.preview} /> )}</div> {/*只有图片有效*/}
                </div> : null}
            </div>
        );
    }
});


//布局也在app里做 app是应用的概念 一个页面可以视为一个应用
class App extends Component {
  render() {
    return (
      <div className="App">
        <div className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h2>文件管理系统（with react）</h2>
        </div>
        <p className="App-intro">
        欢迎使用文件管理系统
        </p>
        {/*记得加大括号,多行注释也是这个
         */}

         <DropzoneDemo />
      </div>
    );
  }
}

export default App;
