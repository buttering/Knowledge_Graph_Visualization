<template>
  <div id="edit-bar" v-if="clicked">
    <div id="type_id">
      <span id="clicked_ele_type">{{ clicked_ele_type }}</span>
      <span id="clicked_ele_id">{{ '#' + clicked_ele_id }}</span>
    </div>

    <div class="clear"></div>

    <div class="line_01"></div>

    <div id="labels">
      <div>{{clicked_ele_label}}</div>
    </div>

    <div class="clear"></div>

    <div id="add_delete">
      <button id="add_node" @click="add_node">添加{{clicked_ele_type}}</button>
      <button id="delete_node" @click="delete_edge">删除此{{clicked_ele_type}}</button><div/>
    </div>

    <div id="Attribute">
      <AttributeItem
          v-for="(value, key) in clicked_ele_attribute"
          :key="key"
          :attr_key="key"
          :attr_value="value"
      ></AttributeItem>

    </div>
    <button @click="edit_node_attribute">edit_node_attribute</button>
    <button @click="delete_node">delete_node</button><div/>
    <button @click="add_edge">add_edge</button>
    <button @click="edit_edge_attribute">edit_edge_attribute</button>

    <div>clicked_eld_id: {{clicked_ele_id}}</div>
  </div>
</template>

<script>
import AttributeItem from "@/components/AttributeItem";
import config from "../../config";
import axios from "axios";

export default {
  name: "EditBar",
  data(){
    return {
      new_ele_type: "",
      new_ele_attribute: {},
      new_edge_source_id: -1,
      new_edge_target_id: -1,
    }
  },
  props:{
    clicked: Boolean,
    clicked_ele_id: Number,
    clicked_ele_type: String,
    clicked_ele_label: String,
    clicked_ele_attribute: Object
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
    }
  },
  components:{
    AttributeItem
  }
}
</script>

<style scoped>
div{
  font-family: Source Han Sans CN,serif;
}
#edit-bar{
  position: fixed;
  right: 5%;
  top: 50%;
  transform:translate(0px,-50%);
  height: 70%;
  width: 300px;
  background: rgba(243, 248, 251, 0.6);
}
#clicked_ele_type{
  font-size: 25px;
  float: left;
  margin-left: 5%;
  margin-top: 10px;
  color: #F3F8FB;

}
#clicked_ele_id{
  font-size: 20px;
  float: right;
  margin-right: 5%;
  margin-top: 20px;
  color: #B9E8F8
}
#labels{
  margin-left: 5%;
  margin-right: 5%;
  width: 100%;

}
#labels div{
  float: left;
  color: black;
  background: orangered;
  height: 20px;
  width: 70px;
  border-radius: 10px;
}
#add_delete{
  width: 90%;
  margin: 5%;
  display: flex;
}
#add_delete button{
  flex: 1;
  border: 0;
  padding: 0;
  height: 40px;
}
#add_node{
  background: green;
}
#delete_node{
  background: red;
}
.line_01{
  margin: 5%;
  border: 1px solid black;
  height: 0;
}
.clear{
  clear: both;
}
</style>