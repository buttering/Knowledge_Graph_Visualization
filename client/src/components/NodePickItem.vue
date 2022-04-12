<template>
  <button id="button" @click="add_node">{{label}}</button>
</template>

<script>
export default {
  name: "NodePickItem",
  props: {
    label: String
  },
  methods: {
    add_node(){
      this.$emit("add_element", "节点", this.label)
    }
  }
}
</script>

<style scoped>
#button{
  width: 100px;
  height: 100px;
  margin: 5px;
  border: 0;
  border-radius: 50%;
  font-size: 100%;
  font-weight: 700;
  font-family: Source Han Sans CN,serif;
  line-height: 0;
  transition-duration: 0.2s;
  cursor: pointer;
  color: #FFFFFF;
}
#button:hover{
  background-color: #FFFFFF !important;
  color: #000000;
}

</style>