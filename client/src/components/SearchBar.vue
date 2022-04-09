<template>
  <div id="search-menu">
    <button id="input" @click="list_element">点击选择元素</button>
    <button id="search" @click="search">条件搜索</button>
  </div>
</template>

<script>

export default {
  name: "SearchBar",
  data(){
    return {
      cypher_sentiment: ""
    }
  },
  props: {
    edge_name_list: Array,
    node_name_list: Array
  },
  methods:{
    list_element(){
      
    },
    construct_cypher(){

    },
    search(){
      //TODO：构建搜索语句

      let cypher_sentiment = "MATCH (n)-[r]-(m) RETURN n, r, m"
      let return_type = ["N", "R", "N"]
      this.$emit('inquire', cypher_sentiment, return_type)
      
    }
  }
}
</script>

<style scoped>
#search-menu{
  position: fixed;
  top: 5%;
  left: 50%;
  transform:translate(-50%,0px);
  height: 50px;
  width: 90%;
  display: flex;
  flex-direction: row;
}
#input{
  float: left;
  flex: 10;
  height: 100%;
  outline: none;
  /*border: 1px solid white;*/
  box-sizing: border-box;
  padding-left: 10px;
  background-color: rgba(243, 248, 251, 0.6);
  border-style: none;

}
#search{
  float: right;
  flex: 1;
  height: 100%;
  background-color: #E4F4FC;
  color: black;
  border-style: none;
  outline: none;
  transition-duration: 0.2s;
  cursor: pointer;
  font-family: Source Han Sans CN,serif;
  font-size: 20px;
  font-weight: 700;
  letter-spacing: 2px;
  min-width: 100px;
}
#search:hover{
  background-color: rgb(120, 120, 120);
  color: white;
}
#search:active{
  background-color: #000000;
}
</style>