<template>
  <div class="attribute-item">
    <span class="key">{{attr_key}}</span>
    <span class="value" contenteditable="true" @input="value_input_change">{{attr_value}}</span>
    <el-tooltip
      effect="dark"
      content="设为主属性"
      placement="top"
    >
      <button class="button" id="main_attribute" @click="set_main_attribute"></button>
    </el-tooltip>
    <el-tooltip
      effect="dark"
      content="保存属性"
      placement="top"
    >
      <button class="button" id="save" @click="save_attribute"></button>
    </el-tooltip>
    <el-tooltip
      effect="dark"
      content="删除属性"
      placement="top"
    >
      <button class="button" id="delete" @click="delete_attribute"></button>
    </el-tooltip>
  </div>
</template>

<script>
export default {
  name: "AttributeItem",
  data(){
    return{
      input_text: ""
    }
  },
  props:{
    background_color: String,
    attr_key: String ,
    attr_value: [String, Number]
  },
  methods: {
    value_input_change(event){
      this.input_text = event.target.innerText
    },
    set_main_attribute(){
      this.$emit("set_main_attribute", this.attr_key)
    },
    save_attribute(){
      this.$emit("edit_ele_attribute", this.attr_key, this.input_text)
    },
    delete_attribute(){
      this.$emit("edit_ele_attribute", this.attr_key)
    }
  },
  mounted() {
    this.input_text = this.attr_value
  }
}
</script>

<style scoped>
.attribute-item{
  display: flex;
  margin-bottom: 3px;
  height: auto;
}
.key{
  flex: 1;
  text-align: left;
  vertical-align: center;
  padding-top: 5px;
  padding-left: 2px;
  margin-right: 2px;
  background-color: rgba(256, 256 ,256 ,0.8);
}
.value{
  flex: 2;
  text-align: left;
  vertical-align: middle;
  padding-top: 5px;
  padding-left: 2px;
  background-color: rgba(256, 256 ,256 ,0.8);
  /*允许长单词换到下一行*/
  word-wrap: break-word;
}
.button{
  width: 30px;
  height: 30px;
  vertical-align: middle;
  border: 0;
  cursor: pointer;
}

#main_attribute{
  background: url("../assets/主属性.jpg") no-repeat;
  /*图片大小自适应*/
  background-size: cover;
}
#save{
  background: url("../assets/保存.jpg") no-repeat;
  background-size: cover;
}
#delete{
  background: url("../assets/删除.jpg") no-repeat;
  background-size: cover;
}
</style>