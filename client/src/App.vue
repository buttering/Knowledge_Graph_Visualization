<template>
  <img alt="Vue logo" src="./assets/logo.png">
  <HelloWorld msg="Welcome to Your Vue.js App"/>
  <button @click="send_request">1</button>
  <div>{{msg}}</div>
  <KnowledgeGraph/>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'
import KnowledgeGraph from './components/KnowledgeGraph'
import config from '../config.js'

import axios from 'axios'


export default {
  name: 'App',
  data(){
    return{
      msg: "a"
    }
  },
  props:{
    node_list: Array,
    edge_list: Array
  },
  methods:{
    send_request(){
      console.log('aaa')
      this.msg = 'c'
      axios.get(config.graph_url).then(function (response){
        console.log(response.data)
        alert(response.data)
        alert('aaa')
        this.msg = 'b'
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

    }
  },
  created(){
    axios.get(config.graph_url)
        .then(function (response){
          console.log(response.data)
          alert(response.data)
          alert('aaa')
    })

  },
  components: {
    HelloWorld,
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
  margin-top: 60px;
}
</style>
