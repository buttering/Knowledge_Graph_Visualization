<template>
  <KnowledgeGraph/>
</template>

<script>
import KnowledgeGraph from './components/KnowledgeGraph'



export default {
  name: 'App',
  data(){
    return{

    }
  },
  methods:{

  },
  created(){

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
