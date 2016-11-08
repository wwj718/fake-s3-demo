import React from 'react';
//import RaisedButton from 'material-ui/RaisedButton';
import FloatingActionButton from 'material-ui/FloatingActionButton';
import ContentAdd from 'material-ui/svg-icons/content/add';

//只是想要ui功能，不能通过类属性修改既有按钮
//需要用父子组件的概念吗
const style = {
  marginRight: 20,
};


//传参
const MyAwesomeReactComponent = () => (
    <FloatingActionButton style={style}>
      <ContentAdd />
    </FloatingActionButton>
);

export default MyAwesomeReactComponent;

