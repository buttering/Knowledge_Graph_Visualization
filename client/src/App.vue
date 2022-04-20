<template>
  <KnowledgeGraph
      v-if="is_login"
      :token=token
      :username="username"
      @need_login="to_login"
  />
  <LoginBar
      v-if="!is_login"
      @login="login"
  />
</template>

<script>
import KnowledgeGraph from './components/KnowledgeGraph'
import LoginBar from "@/components/LoginBar";


export default {
  name: 'App',
  data(){
    return{
      is_login: false,
      token: '',
      username: ''
    }
  },
  methods:{
    login(token, username){
      this.is_login = true
      this.token = token
      this.username = username
    },
    to_login(){
      this.is_login = false
      this.token = ''
    }
  },
  created(){

  },
  components: {
    KnowledgeGraph,
    LoginBar
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
