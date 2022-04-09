<template>
    <div class="attribute-item">
    <span class="key">{{attr_key}}</span>
    <span class="value">{{attr_value}}</span>
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
  name: "AddAttributeItem",
  props:{
    attr_key: String,
    attr_value: String
  },
  methods: {
    delete_attribute(){
      this.$emit("delete_attribute", this.attr_key)
    }
  },
  components: {

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
  flex: 3;
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

#delete{
  background: url("../assets/删除.jpg") no-repeat;
  background-size: cover;
}
</style>