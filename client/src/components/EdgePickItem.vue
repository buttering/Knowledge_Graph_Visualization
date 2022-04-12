<template>
  <button id="button" @click="add_edge">{{view_text}}</button>
</template>

<script>
export default {
  name: "EdgePickItem",
  data(){
    return{

    }
  },
  props: {
    type: String,
    direction: String  // "left", "none", or "right"
  },
  computed: {
    view_text(){
      if (this.direction === 'left'){
        return "⟸ " + this.type + " =="
      } else if (this.direction === 'none'){
        return "== " + this.type + " =="
      } else {
        return "== " + this.type + " ⟹"
      }
    }
  },
  methods: {
    add_edge(){
      this.$emit("add_element", "关系", this.type, this.direction)
    }
  }
}
</script>

<style scoped>
#button{
  width: 200px;
  height: 70px;
  margin: 5px;
  border: 0;
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