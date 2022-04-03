<template>
  <button @click="add_node">add_node</button>
  <button @click="edit_node_attribute">edit_node_attribute</button>
  <button @click="delete_node">delete_node</button><div/>
  <button @click="add_edge">add_edge</button>
  <button @click="edit_edge_attribute">edit_edge_attribute</button>
  <button @click="delete_edge">delete_edge</button><div/>
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
      // this.new_ele_type = "family"
      // this.new_ele_attribute = {"time": 1, "lise": "very"}
      // this.new_edge_target_id = 176
      // this.new_edge_source_id = 174
      let data = {
        "Edge-Type": this.new_ele_type,
        "Edge-Attribute": this.new_ele_attribute,
        "Source-Node": this.new_edge_source_id,
        "Target-Node": this.new_edge_target_id
      }
      let url = config.graph_edge_url
      let type = 'post'
      this.send_request(url, data, type)
    },

    edit_node_attribute(){
      this.new_ele_attribute = this.clicked_ele_attribute
      // this.new_ele_attribute = {'name':'Wang', 'age': 13, 'weight': 15}
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
      // this.new_ele_attribute = {"like": "very", "time": 2}
      // TODO:对属性进行修改
      let data = {
        "Edge-Id": this.clicked_ele_id,
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
      this.send_request(url, data, type)
    },

    delete_edge(){
      let data = {
        "Edge-Id": this.clicked_ele_id
      }
      let url = config.graph_edge_url
      let type = 'delete'
      this.send_request(url, data, type)
    },

    test(){
      this.new_ele_type = 'Animal'
      this.new_ele_attribute = {"age": 1, "name": "bob"}
      this.add_node()
      this.new_ele_attribute = {"name": "pop", age: 2}
      this.add_node()
      this.new_ele_attribute = {"name": "kavien", age: 3}
      this.add_node()

    }
  }
}
</script>

<style scoped>

</style>