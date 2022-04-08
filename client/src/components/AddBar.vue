<template>
  <div id="add-bar">
    <el-radio-group id="type-button" v-model="
    new_type">
      <el-radio-button label="节点"/>
      <el-radio-button label="关系"/>
    </el-radio-group>

    <div v-if="show_node_select" id="graphic">
      <button
          class="node-icon"
          id="source"
          @click="select_node('source')"
      >{{source_node_id}}</button>
      <div id="arrow">&nbsp;===>&nbsp;</div>
      <button
          class="node-icon"
          id="target"
          @click="select_node('target')"
      >{{target_node_id}}</button>
    </div>

    <div id="type-label">
      <el-input v-model="new_label_type" :placeholder="label_or_type"></el-input>
    </div>

    <div id="cancel-submit">
      <el-button id="exit" @click="exit_add_mode">取消</el-button>
      <el-button id="submit" @click="submit">提交</el-button>
    </div>
  </div>
</template>

<script>
export default {
  name: "AddBar",
  data(){
    return {
      source_node_id: -1,
      target_node_id: -1,
      select_type: '',  // 选择的是关系的起点("source")还是终点("target")

      new_type: '关系',  // '节点' or '关系'
      new_label_type: ''
    }
  },
  props: {
    select_node_id: Number
  },
  computed:{
    show_node_select(){
      return this.new_type === '关系'
    },
    label_or_type(){
      if (this.new_type === '节点')
        return '节点标签'
      else if (this.new_type === '关系')
        return '关系类型'
      return ''  // 避免ESL检查 =_=
    }
  },
  methods: {
    exit_add_mode(){
      this.$emit("change_mode", 'view')
    },
    select_node(type){
      this.select_type = type
      this.$emit('change_mode', 'select')
    }
  },
  watch: {
    select_node_id: {
      handler(){
        if (this.select_type === 'source')
          this.source_node_id = this.select_node_id
        else if (this.select_type === 'target')
          this.target_node_id = this.select_node_id
      }
    }
  }
}
</script>

<style scoped>
#add-bar{
  position: fixed;
  right: 5%;
  top: 50%;
  transform:translate(0px,-50%);
  height: 70%;
  width: 300px;
  border-radius: 5px;
  background: rgba(243, 248, 251, 0.6);
}
#type-button{
  width: 90%;
  padding: 5%;
}

/deep/ .el-radio-button{
  flex: 1;
}
/deep/ .el-radio-button__inner{
  width: 100%;
}

#graphic{
  display: flex;
  width: 80%;
  padding-left: 10%;
  padding-right: 10%;
  justify-content: space-between;
}
.node-icon{
  width: 70px;
  height: 70px;
  border: 0;
  border-radius: 50%;
  font-size: 30px;
  font-weight: 500;
  font-family: Source Han Sans CN,serif;
  line-height: 0;
  transition-duration: 0.2s;
  cursor: pointer;

}
#graphic button:hover{
  background: #FFFFFF;
}
#source{
  background: #04E474;
}
#target{
  background: #EC2454;
}
#arrow{
  height: 70px;
  line-height: 70px;
  font-size: 30px;
  font-weight: 700;
}

#type-label{
  width: 90%;
  height: 31px;
  padding: 5%;

}

#cancel-submit{
  position: fixed;
  width: 90%;
  bottom: 0;
  display: flex;
  padding: 5%;
}
/deep/ .el-button{
  flex: 1;
  border: 0;
}

</style>