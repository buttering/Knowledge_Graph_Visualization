<template>
  <div id="edit-bar" v-loading="loading"  element-loading-text="修改中">
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
      <button id="add_node" @click="enter_add_mode">添加节点/关系</button>
      <button id="delete_node" @click="delete_ele">删除此{{clicked_ele_type}}</button><div/>
    </div>

    <div id="attribute">
      <AttributeItem
          v-for="(value, key) in clicked_ele_attribute"
          :key="key"
          :attr_key="key"
          :attr_value="value"
          @set_main_attribute="set_main_attribute"
          @edit_ele_attribute="edit_ele_attribute"
      />
      <NewAttributeItem
          @add_attribute="edit_ele_attribute"
      />
    </div>

  </div>
</template>

<script>
import AttributeItem from "@/components/AttributeItem";
import NewAttributeItem from "@/components/NewAttributeItem";

export default {
  name: "EditBar",
  data(){
    return {

    }
  },
  props:{
    // clicked: Boolean,
    clicked_ele_id: Number,
    clicked_ele_type: String,  //'节点' or '关系'
    clicked_ele_label: String,
    clicked_ele_attribute: Object,

    loading: Boolean  // 由父节点控制加载动画
  },
  methods:{

    // add_node(){
    //   let data = {
    //     "Node-Type": this.new_ele_type,
    //     "Node-Attribute": this.new_ele_attribute
    //   }
    //   let url = config.graph_node_url
    //   let type = 'post'
    //   this.send_request(url, data, type)
    // },

    // add_edge(){
    //   // this.new_ele_type = "family"
    //   // this.new_ele_attribute = {"time": 1, "lise": "very"}
    //   // this.new_edge_target_id = 176
    //   // this.new_edge_source_id = 174
    //   let data = {
    //     "Edge-Type": this.new_ele_type,
    //     "Edge-Attribute": this.new_ele_attribute,
    //     "Source-Node": this.new_edge_source_id,
    //     "Target-Node": this.new_edge_target_id
    //   }
    //   let url = config.graph_edge_url
    //   let type = 'post'
    //   this.send_request(url, data, type)
    // },
    enter_add_mode(){
      this.$emit("change_mode", 'add')
    },

    delete_ele(){
      this.$emit('delete_ele')
    },

    // 对元素属性的添加、修改和删除都通add过这个函数
    edit_ele_attribute(key, value=null){
      let attribute = this.clicked_ele_attribute
      if (value === null){  // 只指明属性关键字，删除操作
        delete attribute[key]
      } else {  // 添加和修改
        attribute[key] = value
      }
      this.$emit("edit_ele_attribute", attribute)
    },

    set_main_attribute(key){
      // 只对节点有效
      if (this.clicked_ele_type !== '节点')
        return
      this.$emit("set_main_attribute", this.clicked_ele_label, key)
    }

  },
  components:{
    AttributeItem,
    NewAttributeItem
  },
  watch: {

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
  /*border-radius: 5px;*/
}
#clicked_ele_type{
  font-size: 30px;
  font-weight: 700;
  letter-spacing: 4px;
  float: left;
  margin-left: 5%;
  margin-top: 10px;
  color: #FFFFFF;

}
#clicked_ele_id{
  font-size: 25px;
  float: right;
  margin-right: 5%;
  margin-top: 15px;
  color: #B9E8F8
}
#labels{
  margin-left: 5%;
  margin-right: 5%;
  width: 100%;

}
#labels div{
  float: left;
  color: white;
  background: #ECBC54;
  height: 20px;
  padding-left: 10px;
  padding-right: 10px;
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
  color: #F3F8FB;
  font-family: Source Han Sans CN,serif;
  font-weight: 500;
  font-size: 15px;
  letter-spacing: 1px;
  transition-duration: 0.2s;
  cursor: pointer;
}
#add_delete button:hover{
  color: black;
  background: whitesmoke;
}
#add_delete button:active{
  border: 0;
}
#add_node{
  background: #04E474;
}
#delete_node{
  background: #EC2454;
}
#attribute{
  padding-left: 5%;
  padding-right: 5%;
  margin-bottom: 10px;
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