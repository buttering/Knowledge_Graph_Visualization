<template>
  <div class="attribute-item">
    <span
        class="key"
        contenteditable="true"
        @input="input_key"
    >{{new_attribute_key}}</span>
    <span
        class="value"
        contenteditable="true"
        @input="input_value"
    >{{new_attribute_value}}</span>
    <el-tooltip
      effect="dark"
      content="添加属性"
      placement="bottom"
    >
      <button class="button" id="add_attribute" @click="add_attribute"></button>
    </el-tooltip>

  </div>
</template>

<script>


export default {
  name: "NewAttributeItem",
  data(){
    return{
      new_attribute_key: "",
      new_attribute_value: "",
      new_attribute_not_empty: false
    }
  },
  methods:{
    input_key(event){
      this.new_attribute_key = event.target.innerText
    },
    input_value(event){
      this.new_attribute_value = event.target.innerText
    },
    add_attribute(){
      if (this.new_attribute_key === ''){
        this.$message.warning("属性名不能为空！")
        return
      }
      this.$emit("add_attribute", this.new_attribute_key, this.new_attribute_value)
      this.new_attribute_key = ''
      this.new_attribute_value = ''
    }
  },
  watch:{

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
  word-wrap: break-word;
}
.value{
  flex: 3;
  text-align: left;
  vertical-align: middle;
  padding-top: 5px;
  padding-left: 2px;
  background-color: rgba(256, 256 ,256 ,0.8);
  word-wrap: break-word;
}
.button{
  width: 30px;
  height: 30px;
  vertical-align: middle;
  border: 0;
}
#add_attribute{
  background: url("../assets/添加.jpg") no-repeat;
  background-size: cover;
  cursor: pointer;
}
</style>