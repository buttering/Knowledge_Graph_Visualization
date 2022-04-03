<template>
  <button @click="add_node">ADD NODE</button>
  <button @click="add_edge">REMOVE RELATIONSHIP</button>
  <button @click="edit_attribute">EDIT ATTRIBUTE</button>
  <button @click="delete_ele">DELETE THIS</button>
  <button @click="test">test</button>
  <div>{{clicked_ele_id}}</div>
</template>

<script>
import config from "../../config";
import axios from "axios";

export default {
  name: "ModifyBar",
  data(){
    return {
      new_ele_type: "",
      new_ele_attribute: {},
      new_edge_source_id: -1,
      new_edge_target_id: -1
    }
  },
  props:{
    clicked_ele_id: Number,
    clicked_ele_type: String,
    clicked_ele_attribute: String
  },
  methods:{
    send_request(url, data, type){
      axios({
        method: type,
        url: url,
        data: data
      }).then(function (response){
        if (response.status === 200 && response.data.code === 200){
          alert("add success!")
        }
      })
    },

    add_node(){
      let data = {
        "Node-Type": this.new_ele_type,
        "Node-Attribute": this.new_ele_attribute
      }
      let url = config.graph_node_url
      let type = 'post'
      this.send_request(url, data, type)
    },

    add_edge(){
      let data = {
        "Edge-Type": this.new_ele_type,
        "Edge-Attribute": this.new_ele_attribute,
        "Source_Node": this.new_edge_source_id,
        "Target-Node": this.new_edge_target_id
      }
      let url = config.graph_edge_url
      let type = 'post'
      this.send_request(url, data, type)
    },

    edit_node_attribute(){
      this.new_ele_attribute = this.clicked_ele_attribute
      // TODO:对属性进行修改
      let data = {
        "Node-Id": this.clicked_ele_id,
        "Node-Attribute": this.new_ele_attribute
      }
      let url = config.graph_node_url
      let type = 'put'
      this.send_request(url, data, type)
    },

    edit_edge_attribute(){
      this.new_ele_attribute = this.clicked_ele_attribute
      // TODO:对属性进行修改
      let data = {
        "Edge-Type": this.clicked_ele_id,
        "Edge-Attribute": this.new_ele_attribute
      }
      let url = config.graph_edge_url
      let type = 'put'
      this.send_request(url, data, type)
    },


    delete_node(){
      let data = {
        "Node-Id": this.clicked_ele_id
      }
      let url = config.graph_node_url
      let type = 'delete'
      this.send_request(data, url, type)
    },

    delete_edge(){
      let data = {
        "Edge-Id": this.clicked_ele_id
      }
      let url = config.graph_edge_url
      let type = 'delete'
      this.send_request(data, url, type)
    },

    test(){

    }
  }
}
</script>

<style scoped>

</style>