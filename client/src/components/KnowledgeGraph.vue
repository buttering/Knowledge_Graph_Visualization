<template>
  <div id="chart" style="width: 600px;height:400px;">bbb</div>
  <div>{{query_result}}</div>
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

import * as echarts from 'echarts/core'
import {BarChart} from 'echarts/charts'
import {TitleComponent, GridComponent} from 'echarts/components'
import {CanvasRenderer} from 'echarts/renderers'

export default {
  name: "KnowledgeGraph",
  data(){
    return {
      title: "Knowledge",
      // click_ele_id: 251,
      click_ele_id: -1,
      click_ele_type: "",
      click_ele_attribute: {},
      query_result:{}  // 返回查询结果,用于可视化展示
    }
  },
  props:{
    node_list: Array,
    edge_list: Array
  },
  methods:{
    init_charts(){
        echarts.use([
            BarChart,
            TitleComponent,
            CanvasRenderer,
            GridComponent
        ])
      // const that = this
      if (!this.myChart){
        this.myChart = echarts.init(document.getElementById('chart'), 'dark')
      }

      var option = {
        xAxis: {
          data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        },
        yAxis: {},
        series: [
          {
            type: 'bar',
            data: [23, 24, 18, 25, 27, 28, 25]
          }
        ]
      }
      window.onresize = this.myChart.resize
      this.myChart.setOption(option)

    },

    test_click_node(){
      this.click_ele_id = 1
    },
    test_click_node_2(){
      this.click_ele_id = 2
    }
  },
  watch: {
    // 该回调会在任何被侦听的对象的 property 改变时被调用，不论其被嵌套多深
    query_result: {
      handler(val, old){
        console.log(val, old)
        this.init_charts()
      }
    }
  },
  mounted() {
    this.query_result = {'aaa': 111}
  },
  components: {
    SearchBar,
    EditBar
  }
}
</script>

<style scoped>

</style>