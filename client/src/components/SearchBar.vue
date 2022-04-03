<template>
  <button @click="search">search</button>
</template>

<script>
import axios from "axios";
import config from "../../config";

export default {
  name: "SearchBar",
  data(){
    return {
      edge_list: [],
      node_list: []
    }
  },
  methods:{
    search(){
      let cypher_sentient = "MATCH (n)-[r]-(m) RETURN n, r, m"
      let return_type = ["N", "R", "N"]
      //TODO：构建搜索语句
      var that = this
      axios({
        method: 'post',
        url: config.graph_url,
        data:{
          "Cypher-Sentiment": cypher_sentient,
          "Return-Type": return_type
        }
      }).then(function (response){
        that.node_list = response.data.msg.nodes
        that.edge_list = response.data.msg.edges
      })
    }
  }
}
</script>

<style scoped>

</style>