<template>
  <div id="chart" style="width: 100%;height: 100%"></div>
  <SearchBar
      :node_name_list="node_name_list"
      :edge_name_list="edge_name_list"
  ></SearchBar>
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
import {BarChart, PieChart} from 'echarts/charts'
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
      click_ele_attribute: {}

    }
  },
  props:{
    node_name_list: Array,
    edge_name_list: Array,
    nodes: Array,
    edges: Array
  },
  methods:{
    init_charts(){
        echarts.use([
            BarChart,
            TitleComponent,
            CanvasRenderer,
            GridComponent,
            PieChart
        ])
      let that = this
      if (!this.myChart){
        this.myChart = echarts.init(document.getElementById('chart'), 'dark')
      }

      var option = {
        series: [
          {
            type: 'pie',
            data: [
              {
                value: 335,
                name: '直接访问'
              },
              {
                value: 234,
                name: '联盟广告'
              },
              {
                value: 1548,
                name: '搜索引擎'
              }
            ]
          }
        ]
      };
      this.myChart.setOption(option)
      window.onresize = function (){
        that.myChart.resize()
      }
      // window.onresize = function (){
      //   function getStyle(el, name){
      //     if (window.getComputedStyle){
      //       return window.getComputedStyle(el, null)
      //     }else{
      //       return el.cuttentStyle
      //     }
      //   }
      //   var wi = getStyle()
      // }
    },
  },
  watch: {
    // 该回调会在任何被侦听的对象的 property 改变时被调用，不论其被嵌套多深
    query_result: {
      handler(val, old){
        // TODO:更新图标
        console.log('query_result has changed:', val, old)
      }
    }
  },
  mounted() {
    this.init_charts()
    // TODO:查询所有元素
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