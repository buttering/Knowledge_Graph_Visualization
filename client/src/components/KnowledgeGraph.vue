<template>
  <div>{{title}}</div>
  <button @click="test_click_node">click node 1</button>
  <button @click="test_click_node_2">click node 2</button>
  <SearchBar></SearchBar>
  <div></div>
  <edit-bar
      :clicked_ele_id="click_ele_id"
      :clicked_ele_type="click_ele_type"
      :clicked_ele_attribute="click_ele_attribute"
  ></edit-bar>
</template>

<script>
import SearchBar from "@/components/SearchBar";
import EditBar from "@/components/EditBar";


export default {
  name: "KnowledgeGraph",
  data(){
    return {
      title: "Knowledge",
      // click_ele_id: 251,
      click_ele_id: -1,
      click_ele_type: "",
      click_ele_attribute: {}
    }
  },
  props:{
    node_list: Array,
    edge_list: Array
  },
  methods:{
    test_click_node(){
      this.click_ele_id = 1
    },
    test_click_node_2(){
      this.click_ele_id = 2
    }
  },
  components: {
    SearchBar,
    EditBar
  }
}
</script>

<style scoped>

</style>