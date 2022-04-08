<template>
  <div id="add-bar">
    <button id="exit" @click="exit_add_mode">exit</button>
    <button id="select_source" @click="select_node('source')">select_source</button>
    <div>{{select_type}},{{ source_node_id}}</div>
  </div>
</template>

<script>
export default {
  name: "AddBar",
  data(){
    return {
      source_node_id: -1,
      target_node_id: -1,
      select_type: ''  // 选择的是关系的起点("source")还是终点("target")
    }
  },
  props: {
    select_node_id: Number
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
  background: rgba(243, 248, 251, 0.6);
}
</style>