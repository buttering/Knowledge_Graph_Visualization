<template>
  <div id="search-menu">
    <button id="input" @click="control_built_bar">{{generate_show_statement}}</button>
    <button id="clear" @click="clear_statement">清除语句</button>
    <button id="search" @click="search">条件搜索</button>
  </div>

  <div v-show="show_built_bar">
    <div id="cypher-bar">
      <el-scrollbar id="nodes">
        <NodePickItem
            v-for="(item, key) in node_name_list"
            class="node button"
            :style="{backgroundColor: random_color()}"
            :key="key"
            :label="item"
            @add_element="add_element"
        />
      </el-scrollbar>

      <el-scrollbar id="edges">
        <EdgePickItem
            v-for="(item, key) in edge_name_list_with_direction"
            class="edge button"
            :style="{backgroundColor: random_color()}"
            :key="key"
            :type="item.type"
            :direction="item.direction"
            @add_element="add_element"
        />
      </el-scrollbar>
    </div>
  </div>

</template>

<script>
import NodePickItem from "@/components/NodePickItem";
import EdgePickItem from "@/components/EdgePickItem";

export default {

  name: "SearchBar",
  data(){
    return {
      element_list: [],  // 存储node和edge序列，用于构建built_list
      built_list: [],  // 用于构建cypher_statement
      cypher_statement: ""
    }
  },
  props: {
    edge_name_list: Array,
    node_name_list: Array,
    show_built_bar: Boolean
  },
  computed:{
    edge_name_list_with_direction(){
      let list = []
      for (let index in this.edge_name_list){
        list.push({
          type: this.edge_name_list[index],
          direction: "none"
        });
        list.push({
          type: this.edge_name_list[index],
          direction: "right"
        });
        list.push({
          type: this.edge_name_list[index],
          direction: "left"
        });
      }
      return list
    },
    generate_show_statement(){  // 展示给用户的字符
      if (this.built_list.length <= 0){
        return "点击图标选择元素"
      }
      let statement = ""
      for (let i = 0; i < this.built_list.length; i++){
        if (this.built_list[i].type === '节点'){
          statement += "( " + this.built_list[i].key + " )"
        } else if (this.built_list[i].direction === 'none'){
          statement += '──[ ' + this.built_list[i].key + ' ]──'
        } else if (this.built_list[i].direction === 'left'){
          statement += '←─[ ' + this.built_list[i].key + ' ]──'
        } else {
          statement += '──[ ' + this.built_list[i].key + ' ]─→'
        }
      }
      return statement
    }
  },
  methods:{
    control_built_bar(){
      this.$emit("change_mode", 'built')
    },
    clear_statement(){
      this.element_list = []
      this.built_list = []
    },
    search(){
      //TODO：构建搜索语句

      let cypher_statement = "MATCH (n)-[r]-(m) RETURN n, r, m"
      let return_type = ["N", "R", "N"]
      this.$emit('inquire', cypher_statement, return_type)
      
    },
    random_color(){
      let col = "#";
      for (let i = 0; i < 6; i++)
        col+=parseInt(Math.random() * 6 + 7).toString(16);
      return col;
    },
    add_element(type, label_or_type, direction=''){
      if (type === null || label_or_type === null)
        return
      this.element_list.push({type: type, key: label_or_type, direction: direction})

      let list = []
      for (let i = 0; i < this.element_list.length; i++) {
        let last_built_type = null
        let current_element = this.element_list[i]
        if (list.length > 0)
          last_built_type = list[list.length - 1].type
        if (current_element.type === last_built_type) {
          // 先插入一个空元素作为占位
          list.push(last_built_type === '节点' ? {type: '关系', key: '', direction: 'none'} : {type: '节点', key: '', direction: ''})
        }
        list.push({type: current_element.type, key: current_element.key, direction: current_element.direction})
      }
      if (list[0].type === '关系')
        list.unshift({type: '节点', key: '', direction: ''})
      if (list[list.length - 1].type === '关系')
        list.push({type: '节点', key: '', direction: ''})
      this.built_list = list
    }
  },
  components: {
    NodePickItem,
    EdgePickItem
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
  box-sizing: border-box;
  padding-left: 10px;
  background-color: rgba(243, 248, 251, 0.6);
  border-style: none;
  font-family: Source Han Sans CN,serif;
  font-weight: 700;
  font-size: 15px;
}
#clear{
  float: left;
  flex: 1;
  height: 100%;
  background-color: #FC9C9C;
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
#clear:hover{
  background-color: rgb(120, 120, 120);
  color: white;
}
#search:hover{
  background-color: rgb(120, 120, 120);
  color: white;
}
#clear:active{
  background-color: #000000;
}
#search:active{
  background-color: #000000;
}

#cypher-bar{
  position: fixed;
  top: 11%;
  left: 50%;
  transform:translate(-50%,0px);
  height: 70%;
  width: 90%;
  display: flex;
  flex-direction: row;
  background-color: rgba(243, 248, 251, 0.6);
}
#nodes{
  margin: 3%;
  margin-right: 1%;
  height: 90%;
  flex: 1;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: flex-start;
  background-color: rgba(256,256,256,0.2);
}
#edges{
  margin: 3%;
  margin-left: 1%;
  height: 90%;
  flex: 1;
  flex-wrap: wrap;
  justify-content: flex-start;
  background-color: rgba(256,256,256,0.2);
}

.node{

}
.edge{

}
.line{
  margin-top: 3%;
  margin-bottom: 3%;
  border: 1px solid black;
  height: 93%;
  width: 0;
}
</style>