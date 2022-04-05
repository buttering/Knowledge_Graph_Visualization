<template>
  <div id="search-menu">
    <input placeholder="请输入...">
    <button class='button' id="search" @click="search">search</button>
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
    search(){
      //TODO：构建搜索语句
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
  background: rgba(104,104,104, 0.26);
  display: flex;
  flex-direction: row;
}
#search-menu input{
  float: left;
  flex: 1;
  height: 100%;
  outline: none;
  border: 1px solid white;
  box-sizing: border-box;
  padding-left: 10px;

}
#search-menu button{
  float: right;
  flex: 0;
  height: 100%;
  background-color: rgb(224, 224, 224);
  color: black;
  border-style: none;
  outline: none;
  transition-duration: 0.2s;
  cursor: pointer
}
#search-menu button:hover{
  background-color: rgb(120, 120, 120);
  color: white;
}
#search-menu button:active{
  background-color: #000000;
}
</style>