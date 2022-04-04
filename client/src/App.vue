<template>
  <KnowledgeGraph
      :node_name_list="node_name_list"
      :edge_name_list="edge_name_list"
      :nodes="nodes"
      :edges="edges"
  ></KnowledgeGraph>
</template>

<script>
import KnowledgeGraph from './components/KnowledgeGraph'

import config from '../config.js'

import axios from 'axios'


export default {
  name: 'App',
  data(){
    return{
      // 以下两个变量需要传递给SearchBar
      node_name_list: [],
      edge_name_list: [],
      // 以下两个两个变量传递给KnowledgeGraph
      nodes: [],
      edges: []
    }
  },
  methods:{

  },
  created(){
    var that = this
      axios.get(config.graph_url).then(function (response){
        // 回调函数中this指向会改变，所以先用that保存Vue对象指针
        that.node_name_list = response.data.msg.node_name_list
        that.edge_name_list = response.data.msg.edge_name_list
        that.nodes = response.data.msg.nodes
        that.edges = response.data.msg.edges
        console.log(response.data.msg)
      }).catch(error=>{
        if (error.response) {
          // 请求已发出，且服务器的响应状态码超出了 2xx 范围
          console.log(error.response.data);
          console.log(error.response.status);
          console.log(error.response.headers);
        } else if (error.request) {
          // 请求已发出，但没有接收到任何响应
          // 在浏览器中，error.request 是 XMLHttpRequest 实例
          // 在 node.js 中，error.request 是 http.ClientRequest 实例
          console.log(error.request);
        } else {
            // 引发请求错误的错误信息
            console.log('Error', error.message);
        }
        console.log(error.config);
    });

  },
  components: {
    KnowledgeGraph
  }
}
</script>

<style>
  #app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
  }
  html,body,#app{
    height: 100%;
    width: 100%
}
</style>
